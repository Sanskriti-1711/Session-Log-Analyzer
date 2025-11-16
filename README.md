# Session-Log-Analyzer

Language: Python 3.10+
Type: Command-line application
Author: Your Name

📌 Overview

SessionLogProcessor reads an application usage log and computes:

The number of sessions per user

The minimum possible total duration of their sessions

While handling missing Start/End events, overlapping sessions, and invalid log lines

This tool implements all rules from the coding challenge specification and guarantees output consistent with the minimum possible interpretation of session durations.


✔️ Problem Summary

The log file contains lines like:

HH:MM:SS USER Start
HH:MM:SS USER End


🛠️ How to Build & Run

There is no build step.
The program is a pure Python script run directly from the command line.

Run Command
python session_report.py path/to/logfile.txt



🧠 Rules Implemented in the Code

✔️ Valid Line

A line must contain exactly:

HH:MM:SS  USERNAME  Start|End


otherwise it is ignored.

✔️ Missing Start

If an End is encountered with no available Start, the Start time is assumed to be the earliest timestamp in the file.

✔️ Missing End

If a Start remains unmatched after reading the entire file, its End time becomes the latest timestamp in the file.

✔️ Overlapping Sessions

Managed using a LIFO stack per user.

Example:

Start
Start
End → matches latest Start
End → matches remaining Start

✔️ Invalid or Irrelevant Lines

Silently ignored, per the problem specification.

✔️ Output

Sorted alphabetically by username.
