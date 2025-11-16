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


But:

Start and End are not paired

Some sessions may be missing Start or End

Sessions may overlap

Some lines may be invalid and must be ignored

Log boundaries may cut off earlier/later sessions

The program must reconstruct a consistent, minimum-duration explanation and report:

USERNAME SESSIONS TOTAL_DURATION_SECONDS


Sorted alphabetically by username.
