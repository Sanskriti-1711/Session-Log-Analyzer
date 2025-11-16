import sys

# Converts "HH:MM:SS" to seconds since midnight
def parse_time(time_str):
    try:
        h, m, s = map(int, time_str.split(":"))
        if 0 <= h < 24 and 0 <= m < 60 and 0 <= s < 60:
            return h * 3600 + m * 60 + s
        return None
    except:
        return None


def main():
    # Expects exactly 1 argument from the logfile path
    if len(sys.argv) != 2:
        return 

    logfile_path = sys.argv[1]

    # Try reading the file
    try:
        with open(logfile_path, "r") as f:
            lines = f.read().splitlines()
    except:
        return

    # Parsed valid entries will be stored here
    records = []    # Each item: (time_in_seconds, user, action)

    earliest = None  # Earliest seen timestamp
    latest = None    # Latest seen timestamp

    # --------------------------------------------------------
    # STEP 1: Parse and validate all log lines
    # --------------------------------------------------------
    for raw_line in lines:
        parts = raw_line.strip().split()

        # Valid log line format:  3 tokens → <time> <user> <Start/End>
        if len(parts) != 3:
            continue

        time_str, user, action = parts

        # Validate time
        time_val = parse_time(time_str)
        if time_val is None:
            continue

        # Validate action
        if action not in ("Start", "End"):
            continue

        # Store the clean record
        records.append((time_val, user, action))

        # Track earliest & latest times for unmatched sessions
        if earliest is None or time_val < earliest:
            earliest = time_val
        if latest is None or time_val > latest:
            latest = time_val

  
    # Data structures per user
    # For overlapping Start events, we use a stack
    starts = {}      # user → stack of unclosed start times
    durations = {}   # user → total accumulated duration
    sessions = {}    # user → number of sessions counted

    # --------------------------------------------------------
    # STEP 2: Process Start/End pairs in chronological order
    # --------------------------------------------------------
    for time_val, user, action in sorted(records):
        # Initialize user tracking if first appearance
        if user not in starts:
            starts[user] = []
            durations[user] = 0
            sessions[user] = 0

        if action == "Start":
            # Push this start timestamp on the user's stack
            starts[user].append(time_val)

        elif action == "End":
            # If user has an unmatched Start, pop it
            if starts[user]:
                start_time = starts[user].pop()
            else:
                # If we have an End without Start, assume they started at earliest possible time
                start_time = earliest

            durations[user] += time_val - start_time
            sessions[user] += 1

    # --------------------------------------------------------
    # STEP 3: Handle any users with unmatched Start events
    # (These get auto-closed at the latest timestamp)
    # --------------------------------------------------------
    for user in starts:
        while starts[user]:
            start_time = starts[user].pop()
            durations[user] += latest - start_time
            sessions[user] += 1

    # --------------------------------------------------------
    # STEP 4: Output final user summary sorted alphabetically
    # --------------------------------------------------------
    for user in sorted(durations.keys()):
        print(f"{user} {sessions[user]} {durations[user]}")


if __name__ == "__main__":
    main()
