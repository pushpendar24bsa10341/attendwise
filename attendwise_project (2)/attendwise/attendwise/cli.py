"""Command-line menu (user interaction layer)."""
from .exceptions import AttendWiseError
from .logger import get_logger
from .manager import AttendanceManager
from .reports import bunk_calculator, build_report, export_csv, whatif_report
from .validators import validate_count

log = get_logger()

MENU = """
========== AttendWise ==========
 1. Add subject
 2. Log a class (present / absent)
 3. Undo last logged class
 4. Attendance report
 5. Bunk calculator (skip / attend)
 6. What-if planner (semester forecast)
 7. Update subject counts / remaining classes
 8. Set required attendance %
 9. Remove subject
10. Export report to CSV
 0. Exit
"""


def handle_choice(choice, m):
    """Run one menu action. Raises AttendWiseError on invalid input."""
    if choice == "1":
        s = m.add_subject(input("Subject name: "),
                          input("Classes attended so far [0]: ") or 0,
                          input("Total classes held so far [0]: ") or 0,
                          input("Classes remaining this semester [0]: ") or 0)
        print(f"Added {s.name}.")
    elif choice == "2":
        s = m.log_class(input("Subject: "), input("Present or Absent (P/A): "),
                        input("Date YYYY-MM-DD (blank = today): "))
        print(f"Logged. {s.name} is now {s.attended}/{s.total} = {s.percentage():.1f}%")
    elif choice == "3":
        r = m.undo_last(input("Subject: "))
        print(f"Removed entry: {r.day} {'present' if r.present else 'absent'}")
    elif choice == "4":
        print("\n" + build_report(m.subjects, m.threshold))
    elif choice == "5":
        print("\n" + bunk_calculator(m.get_subject(input("Subject: ")), m.threshold))
    elif choice == "6":
        s = m.get_subject(input("Subject: "))
        n = validate_count(input(f"How many of the {s.remaining} remaining classes will you miss? "),
                           "Planned absences")
        print("\n" + whatif_report(s, m.threshold, n))
    elif choice == "7":
        m.update_subject(input("Subject: "), input("New attended (blank = keep): "),
                         input("New total (blank = keep): "),
                         input("New remaining (blank = keep): "))
        print("Updated.")
    elif choice == "8":
        m.set_threshold(input("Required attendance % (e.g. 75): "))
        print(f"Threshold is now {m.threshold}%.")
    elif choice == "9":
        m.remove_subject(input("Subject: "))
        print("Removed.")
    elif choice == "10":
        print("Saved to", export_csv(m.subjects, m.threshold, "data/report.csv"))
    else:
        print("Invalid choice. Enter a number from the menu.")


def run():
    manager = AttendanceManager()
    log.info("AttendWise started")
    while True:
        print(MENU)
        try:
            choice = input("Choose: ").strip()
            if choice == "0":
                print("Stay above the line. Bye!")
                log.info("AttendWise closed")
                break
            handle_choice(choice, manager)
        except AttendWiseError as err:        # expected, user-fixable problems
            print(f"Error: {err}")
            log.warning("User error: %s", err)
        except (KeyboardInterrupt, EOFError):
            print("\nInput cancelled. Bye!")
            break
        except Exception as err:               # unexpected bugs: log, do not crash
            print("Something went wrong. Details saved to the log.")
            log.exception("Unexpected error: %s", err)
