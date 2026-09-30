"""Generates all diagrams and sample-output images used in the report (run from project root)."""
import os
import sys
from datetime import date

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, Rectangle

sys.path.insert(0, ".")
OUT = "docs"
BLUE, GREEN, ORANGE, GREY, RED = "#dbe9ff", "#dcf5e3", "#ffe8cc", "#eeeeee", "#ffd9d9"


def canvas(w, h, title):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w * 10); ax.set_ylim(0, h * 10); ax.axis("off")
    ax.set_title(title, fontsize=13, fontweight="bold")
    return fig, ax


def box(ax, x, y, w, h, text, color=BLUE, fs=9, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4", fc=color, ec="#333", lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal")


def arrow(ax, p1, p2, text="", style="->", ls="-"):
    ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle=style, lw=1.3, color="#333", linestyle=ls))
    if text:
        ax.text((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 1.2, text, fontsize=7.5, ha="center",
                bbox=dict(fc="white", ec="none", pad=0.5))


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=100, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# 1. Architecture ------------------------------------------------------------
def architecture():
    fig, ax = canvas(10, 7.2, "System Architecture (Layered Design)")
    box(ax, 30, 62, 40, 6, "USER (Student) - keyboard input / console output", GREY, bold=True)
    box(ax, 20, 48, 60, 7, "PRESENTATION LAYER\ncli.py (menu)  |  main.py (entry point)", BLUE, bold=True)
    box(ax, 4, 26, 28, 14, "MODULE 1\nmanager.py\nSubject CRUD + logging classes", GREEN)
    box(ax, 36, 26, 28, 14, "MODULE 2\npredictor.py\nSkip / attend / forecast maths", GREEN)
    box(ax, 68, 26, 28, 14, "MODULE 3\nreports.py\nReports, what-if, CSV export", GREEN)
    box(ax, 4, 8, 22, 9, "models.py\nSubject, Record", ORANGE)
    box(ax, 30, 8, 22, 9, "validators.py\nexceptions.py", ORANGE)
    box(ax, 56, 8, 18, 9, "storage.py\n(JSON)", ORANGE)
    box(ax, 78, 8, 18, 9, "logger.py\n(log file)", ORANGE)
    arrow(ax, (50, 62), (50, 55.6)); arrow(ax, (35, 48), (18, 40.6)); arrow(ax, (50, 48), (50, 40.6)); arrow(ax, (65, 48), (82, 40.6))
    arrow(ax, (18, 26), (15, 17.6)); arrow(ax, (25, 26), (38, 17.6)); arrow(ax, (30, 26), (62, 17.6)); arrow(ax, (10, 26), (85, 17.6), ls=":")
    arrow(ax, (68, 33), (64.3, 33), "", ls=":")
    ax.text(50, 2, "Data files: data/attendance.json  |  data/report.csv  |  data/attendwise.log", ha="center", fontsize=8.5, style="italic")
    save(fig, "architecture.png")


# 2. Workflow ----------------------------------------------------------------
def workflow():
    fig, ax = canvas(11, 10, "Workflow Diagram")
    for text, c, y in [("Start program", GREY, 88), ("Load saved data\n(or start empty)", BLUE, 78),
                       ("Show menu, read choice", BLUE, 68)]:
        box(ax, 25, y, 40, 6, text, c)
    arrow(ax, (45, 88), (45, 84.4)); arrow(ax, (45, 78), (45, 74.4))
    ax.add_patch(plt.Polygon([(45, 64), (65, 56), (45, 48), (25, 56)], fc=ORANGE, ec="#333"))
    ax.text(45, 56, "Choice valid?", ha="center", va="center", fontsize=9)
    arrow(ax, (45, 68), (45, 64))
    box(ax, 72, 52, 24, 8, "Print error,\nreturn to menu", RED)
    arrow(ax, (65, 56), (72, 56), "No")
    box(ax, 25, 34, 40, 8, "Validate inputs\n(counts, names, dates, P/A)", BLUE)
    arrow(ax, (45, 48), (45, 42.4), "Yes")
    ax.add_patch(plt.Polygon([(45, 30), (63, 24), (45, 18), (27, 24)], fc=ORANGE, ec="#333"))
    ax.text(45, 24, "Input OK?", ha="center", va="center", fontsize=9)
    arrow(ax, (45, 34), (45, 30))
    arrow(ax, (63, 24), (72, 24), "No")
    box(ax, 72, 20, 24, 8, "Show message\n+ write log", RED)
    box(ax, 25, 6, 40, 8, "Run action: update data / predict /\nreport -> save to JSON -> print result", GREEN)
    arrow(ax, (45, 18), (45, 14.4), "Yes")
    # return loops (kept clear of every box)
    ax.plot([84, 84], [60.5, 71], color="#333", lw=1.2)            # error box top -> up
    ax.plot([96.5, 100, 100], [24, 24, 71], color="#333", lw=1.2)  # message box right -> up
    ax.plot([84, 100], [71, 71], color="#333", lw=1.2)
    arrow(ax, (84, 71), (65.6, 71))
    ax.plot([25, 12, 12], [10, 10, 71], color="#333", lw=1.2); arrow(ax, (12, 71), (24.4, 71))
    ax.text(11, 40, "success: back to menu", rotation=90, fontsize=8, va="center", ha="right")
    ax.text(45, 1, "Choice 0 (Exit) leaves the loop and ends the program.", ha="center", fontsize=8, style="italic")
    save(fig, "workflow.png")


# 3. Use case ----------------------------------------------------------------
def usecase():
    fig, ax = canvas(10, 8, "Use Case Diagram")
    ax.add_patch(Rectangle((28, 4), 64, 72, fc="white", ec="#333", lw=1.5))
    ax.text(60, 77.5, "AttendWise System", ha="center", fontsize=10, fontweight="bold")
    cases = ["Add / update / remove subject", "Log a class (present/absent)", "Undo last logged class",
             "View attendance report", "Use bunk calculator", "Run what-if semester planner",
             "Set required attendance %", "Export report to CSV"]
    ys = [68, 60, 52, 44, 36, 28, 20, 12]
    for text, y in zip(cases, ys):
        ax.add_patch(Ellipse((60, y), 46, 6.5, fc=BLUE, ec="#333"))
        ax.text(60, y, text, ha="center", va="center", fontsize=8.5)
        arrow(ax, (13, 40), (37, y), style="-")
    ax.add_patch(Ellipse((13, 46), 4, 5, fc="white", ec="black", lw=1.5)); ax.plot([13, 13], [43, 36], "k", lw=1.5)
    ax.plot([9, 17], [41, 41], "k", lw=1.5); ax.plot([13, 9], [36, 31], "k", lw=1.5); ax.plot([13, 17], [36, 31], "k", lw=1.5)
    ax.text(13, 27, "Student", ha="center", fontsize=10, fontweight="bold")
    save(fig, "usecase.png")


# 4. Sequence ----------------------------------------------------------------
def sequence():
    fig, ax = canvas(11, 8, "Sequence Diagram: Log a Class, then View Report")
    names = ["Student", "CLI", "Manager", "Validators", "Storage", "Predictor/Reports"]
    xs = [8, 27, 46, 64, 81, 98]
    for n, x in zip(names, xs):
        box(ax, x - 8, 72, 16, 4, n, BLUE, fs=8.5, bold=True)
        ax.plot([x, x], [70, 4], color="#888", ls="--", lw=1)
    msgs = [(0, 1, 66, "choose 2 (log class)"), (1, 2, 61, "log_class(name, 'P', date)"),
            (2, 3, 56, "validate_present / validate_date"), (3, 2, 52, "clean values", True),
            (2, 2, 47, "Subject.log_class()"), (2, 4, 42, "save_data()"),
            (2, 1, 37, "updated subject", True), (1, 0, 33, "'Logged: 19/21 = 90.5%'", True),
            (0, 1, 27, "choose 4 (report)"), (1, 5, 22, "build_report(subjects, threshold)"),
            (5, 5, 17, "status(), advice()"), (5, 1, 12, "report text", True), (1, 0, 8, "print report", True)]
    for m in msgs:
        a, b, y, text = m[:4]; dashed = len(m) > 4
        if a == b:
            ax.annotate("", xy=(xs[a] + 0.5, y - 2), xytext=(xs[a] + 0.5, y), arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-1.2"))
            ax.text(xs[a] + 3, y - 1, text, fontsize=7.5)
        else:
            arrow(ax, (xs[a], y), (xs[b], y), text, ls="--" if dashed else "-")
    save(fig, "sequence.png")


# 5. Class diagram -----------------------------------------------------------
def classdiagram():
    fig, ax = canvas(11, 7.5, "Class / Component Diagram")
    def cls(x, y, w, h, title, body, color=BLUE):
        ax.add_patch(Rectangle((x, y), w, h, fc=color, ec="#333", lw=1.3))
        ax.add_patch(Rectangle((x, y + h - 5), w, 5, fc="#bcd3f5", ec="#333", lw=1.3))
        ax.text(x + w / 2, y + h - 2.5, title, ha="center", va="center", fontweight="bold", fontsize=9)
        ax.text(x + 1.2, y + h - 7, body, va="top", fontsize=7.6, family="monospace")
    cls(2, 34, 34, 38, "Subject",
        "- name: str\n- attended: int\n- total: int\n- remaining: int\n- history: list[Record]\n"
        "+ percentage()\n+ log_class(present, day)\n+ undo_last()\n+ to_dict() / from_dict()")
    cls(44, 50, 26, 22, "Record", "- day: date\n- present: bool\n+ to_dict()\n+ from_dict()")
    cls(2, 2, 40, 27, "AttendanceManager",
        "- path, threshold\n- subjects: list[Subject]\n+ add_subject() / update_subject()\n+ remove_subject()\n"
        "+ log_class() / undo_last()\n+ set_threshold()", GREEN)
    cls(48, 2, 30, 27, "predictor (functions)",
        "classes_can_skip()\nclasses_needed()\nstatus()\nforecast()\nsemester_outlook()\nadvice()", ORANGE)
    cls(82, 2, 26, 27, "reports (functions)", "build_report()\nbunk_calculator()\nwhatif_report()\nexport_csv()", ORANGE)
    cls(78, 34, 30, 38, "Support modules",
        "storage: load_data()\n         save_data()\nvalidators: validate_*()\nexceptions: AttendWiseError\n   +ValidationError\n   +NotFoundError\n   +DuplicateError\n   +StorageError\nlogger: get_logger()", GREY)
    arrow(ax, (36, 60), (44, 60), "1..*", style="-|>"); ax.text(37, 62.5, "has", fontsize=7.5)
    arrow(ax, (20, 29), (20, 34), "manages", style="-|>")
    arrow(ax, (82, 15), (78.4, 15), "uses", ls=":")
    arrow(ax, (42, 27), (78, 40), "uses", ls=":")
    save(fig, "classdiagram.png")


# 6. ER ----------------------------------------------------------------------
def er():
    fig, ax = canvas(10, 3.9, "ER Diagram (JSON storage: attendance.json)")
    def ent(x, y, title, attrs):
        h = 8 + 4.2 * len(attrs)
        ax.add_patch(Rectangle((x, y), 26, h, fc="white", ec="#333", lw=1.3))
        ax.add_patch(Rectangle((x, y + h - 5), 26, 5, fc=BLUE, ec="#333", lw=1.3))
        ax.text(x + 13, y + h - 2.5, title, ha="center", va="center", fontweight="bold", fontsize=9.5)
        for i, a in enumerate(attrs):
            ax.text(x + 1.5, y + h - 8 - 4.2 * i, a, fontsize=8.2, va="center")
    ent(3, 6, "SETTINGS", ["PK  id (single record)", "threshold : int (1-100)"])
    ent(37, 6, "SUBJECT", ["PK  name : str (unique)", "attended : int", "total : int", "remaining : int"])
    ent(70, 6, "RECORD", ["PK  record_id (list index)", "FK  subject_name", "date : YYYY-MM-DD", "present : bool"])
    arrow(ax, (63, 17), (70, 17), "1 : N", style="-")
    arrow(ax, (29, 14), (37, 14), "applies to", style="-")
    ax.text(50, 0.5, "Constraint: attended <= total, all counts >= 0", ha="center", fontsize=8, style="italic")
    save(fig, "er.png")


# 7. Terminal-style sample outputs ------------------------------------------
def terminal(name, text, w=11):
    lines = text.split("\n")
    h = 0.16 * len(lines) + 0.4
    fig = plt.figure(figsize=(w, h), facecolor="#1e1e1e")
    fig.text(0.02, 0.97, "\n".join(lines), family="monospace", color="#e6e6e6", fontsize=9, va="top")
    fig.savefig(os.path.join(OUT, name), dpi=130, facecolor="#1e1e1e")
    plt.close(fig)


def samples():
    from attendwise.models import Subject
    from attendwise.reports import bunk_calculator, build_report, whatif_report
    subs = [Subject("Python", 19, 21, 30), Subject("Maths", 12, 20, 30), Subject("Physics", 15, 20, 30)]
    terminal("shot_report.png", ">>> Menu option 4: Attendance report\n\n" + build_report(subs, 75), 7.6)
    terminal("shot_predict.png", ">>> Menu option 5: Bunk calculator (Maths)\n\n" + bunk_calculator(subs[1], 75) +
             "\n\n>>> Menu option 6: What-if planner (Physics, miss 2)\n\n" + whatif_report(subs[2], 75, 2), 6.4)
    terminal("shot_errors.png",
             ">>> Add subject with attended > total\nError: Classes attended cannot be more than total classes held.\n\n"
             ">>> Log class with input 'maybe'\nError: Enter P for present or A for absent.\n\n"
             ">>> Log class for a future date\nError: You cannot log a class for a future date.\n\n"
             ">>> Bunk calculator for unknown subject 'Chemistry'\nError: Subject 'Chemistry' not found.\n\n"
             ">>> Set required attendance to 150\nError: Required percentage must be between 1 and 100.", 6.6)


if __name__ == "__main__":
    for fn in (architecture, workflow, usecase, sequence, classdiagram, er, samples):
        fn()
    print("done")
