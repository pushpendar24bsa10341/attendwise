# AttendWise - Attendance Shortage Predictor

A command-line Python program that tells a student **how many more classes they can safely skip**
in each subject, or **how many they must attend in a row** to get back above the required
attendance percentage. Built for the *Python Essentials* course project at VIT Bhopal University.

## Overview
Colleges usually ask for 75% attendance. AttendWise keeps your attended/held counts for every
subject, lets you log each class as present or absent, and works out how many classes you can
skip, how many you need to recover, and where you will end up at the end of the semester.

## Features
- Add, update and remove subjects with their attendance counts (full CRUD)
- Log a class as present/absent (with date) and undo the last entry
- **Bunk calculator**: classes you can still skip / must attend in a row
- **What-if planner**: final percentage if you miss N of the remaining classes
- Status per subject: `SAFE`, `WARNING`, `SHORTAGE`, `NO DATA`
- Attendance report with overall percentage and shortage alerts
- Configurable required percentage (default 75%)
- Export report to CSV
- Input validation, custom exceptions, logging, safe saves and corrupt-file recovery

## How the prediction works
Let `a` = classes attended, `t` = classes held, `T` = required %.

| Question | Formula |
|---|---|
| Classes you can still skip | `floor(100*a / T) - t` (never below 0) |
| Classes to attend in a row | `ceil((T*t - 100*a) / (100 - T))` |

Example (T = 75): attended 6 of 10 (60%) -> attend the next **6** classes in a row (12/16 = 75%).
Only integer arithmetic is used, so the results are exact. The tests check both formulas
against brute-force loops.

## Technologies / tools used
- Python 3.8+ (standard library only: `json`, `csv`, `logging`, `datetime`, `os`)
- `unittest` for testing
- Git and GitHub for version control
- No third-party packages are needed to run the project

## Project structure
```
attendwise/
├── main.py                 # entry point
├── attendwise/
│   ├── cli.py              # menu / user interaction
│   ├── manager.py          # Module 1: subject CRUD + class logging
│   ├── predictor.py        # Module 2: prediction maths
│   ├── reports.py          # Module 3: reports, what-if, CSV export
│   ├── models.py           # Subject and Record classes
│   ├── storage.py          # JSON load/save
│   ├── validators.py       # input validation
│   ├── exceptions.py       # custom exceptions
│   └── logger.py           # logging setup
├── tests/                  # unit tests (27 tests)
├── docs/                   # diagrams + diagram generator script
├── data/                   # saved data, log, CSV export (created at run time)
├── statement.md
└── README.md
```

## Steps to install and run
```bash
git clone <your-repo-url>
cd attendwise
python main.py          # use python3 on Linux/macOS
```
No installation is required. Data is saved in `data/attendance.json`.

**Quick start:** choose `8` to set the required % -> `1` to add subjects -> `4` for the report.

## Instructions for testing
```bash
python -m unittest discover -s tests -t . -v
```
All 27 tests should pass. They cover validators, the prediction formulas (including a
brute-force cross-check), the manager (CRUD, persistence, undo), storage (missing/corrupt
file) and reports (including CSV export).

## Screenshots
See `docs/shot_report.png`, `docs/shot_predict.png` and `docs/shot_errors.png`.

## Author
Pushpendar Singh (24BSA10341)  
B.Tech CSE (Cloud Computing and Automation), VIT Bhopal University  
Python Essentials - VITyarthi
