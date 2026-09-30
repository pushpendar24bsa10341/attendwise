# Problem Statement - AttendWise

## Problem statement
Most colleges require students to keep a minimum attendance percentage (commonly 75%) to be
allowed to write the exams. Students usually track attendance loosely, so they only discover
a shortage when it is already too late. Working out "how many classes can I still skip?" or
"how many classes must I attend to recover?" needs a formula that most students do not
calculate by hand, and mistakes can cost them exam eligibility.

## Scope of the project
**In scope**
- Track attendance for multiple subjects (classes attended vs. classes held).
- Log each class as present/absent with a date, and undo the last entry.
- Predict, per subject, how many classes can still be skipped and how many must be attended
  in a row to reach the required percentage.
- Forecast the end-of-semester percentage for a planned number of absences.
- Report status (SAFE / WARNING / SHORTAGE) and export the report to CSV.
- Persist all data in a local JSON file.

**Out of scope**
- Multi-user accounts, cloud sync, or a web/mobile interface.
- Reading timetables or college portals automatically.

## Target users
- College students who must maintain a minimum attendance percentage.
- Anyone learning Python who wants a small, real-world example of functions, classes,
  file handling and exception handling.

## High-level features
1. **Subject and attendance management** - add, update, remove subjects; log present/absent; undo.
2. **Shortage prediction engine** - exact "can skip" / "must attend" calculations and semester what-if forecast.
3. **Reports and export** - text report with status and advice; CSV export.
4. **Reliability** - input validation, custom exceptions, safe file writes, corrupt-file recovery and logging.
