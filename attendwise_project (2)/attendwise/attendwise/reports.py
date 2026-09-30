"""Module 3 - Reports and CSV export."""
import csv

from . import predictor as p
from .exceptions import StorageError, ValidationError


def build_report(subjects, threshold):
    """Text table with one row per subject plus an overall summary."""
    if not subjects:
        return "No subjects yet."
    lines = [f"Required attendance: {threshold}%",
             f"{'Subject':<16}{'Att/Tot':>9}{'%':>8}  {'Status':<10}Advice",
             "-" * 92]
    for s in subjects:
        lines.append(f"{s.name:<16}{s.attended:>4}/{s.total:<4}{s.percentage():>7.1f}  "
                     f"{p.status(s.attended, s.total, threshold):<10}"
                     f"{p.advice(s.attended, s.total, threshold)}")
    total = sum(s.total for s in subjects)
    att = sum(s.attended for s in subjects)
    lines.append("-" * 92)
    lines.append(f"Overall: {att}/{total} classes = {p.percentage(att, total):.1f}%")
    risky = [s.name for s in subjects if p.status(s.attended, s.total, threshold) == "SHORTAGE"]
    if risky:
        lines.append("ATTENTION - shortage in: " + ", ".join(risky))
    return "\n".join(lines)


def bunk_calculator(subject, threshold):
    """Detailed skip/attend numbers for one subject."""
    a, t = subject.attended, subject.total
    if t == 0:
        return f"{subject.name}: no classes recorded yet."
    need = p.classes_needed(a, t, threshold)
    return (f"{subject.name}: {a}/{t} = {p.percentage(a, t):.1f}% "
            f"[{p.status(a, t, threshold)}]\n"
            f"  Can still skip : {p.classes_can_skip(a, t, threshold)} class(es)\n"
            f"  Must attend    : {'impossible' if need is None else need} class(es) in a row\n"
            f"  {p.advice(a, t, threshold)}")


def whatif_report(subject, threshold, planned_absences):
    """Semester forecast for a planned number of absences."""
    if subject.remaining <= 0:
        raise ValidationError(f"Set remaining classes for {subject.name} first (menu option 7).")
    if not 0 <= planned_absences <= subject.remaining:
        raise ValidationError(f"Planned absences must be between 0 and {subject.remaining}.")
    final = p.forecast(subject.attended, subject.total, subject.remaining, planned_absences)
    outlook = p.semester_outlook(subject.attended, subject.total, subject.remaining, threshold)
    verdict = "PASS" if final * 100 >= threshold * 100 - 1e-9 else "SHORTAGE"
    lines = [f"{subject.name}: {subject.remaining} class(es) remaining",
             f"  If you miss {planned_absences}: final attendance = {final:.1f}%  -> {verdict}"]
    if outlook["achievable"]:
        lines.append(f"  To stay eligible you must attend at least {outlook['must_attend']} "
                     f"and may miss at most {outlook['can_miss']} of them.")
    else:
        lines.append(f"  Even attending all remaining classes cannot reach {threshold}%.")
    return "\n".join(lines)


def export_csv(subjects, threshold, path):
    """Save the report table as a CSV file."""
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Subject", "Attended", "Total", "Percentage", "Status",
                             "Can skip", "Must attend"])
            for s in subjects:
                need = p.classes_needed(s.attended, s.total, threshold)
                writer.writerow([s.name, s.attended, s.total, round(s.percentage(), 1),
                                 p.status(s.attended, s.total, threshold),
                                 p.classes_can_skip(s.attended, s.total, threshold),
                                 "impossible" if need is None else need])
    except OSError as err:
        raise StorageError(f"Cannot write {path}: {err}")
    return path
