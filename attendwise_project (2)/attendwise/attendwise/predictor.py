"""Module 2 - The prediction engine (pure functions, integer maths only).

Let a = classes attended, t = classes held, T = required percentage.

Classes you can still skip (x):   a / (t + x) >= T/100   ->   x = floor(100a / T) - t
Classes you must attend in a row (y):  (a + y) / (t + y) >= T/100
                                        ->   y = ceil((T*t - 100a) / (100 - T))

Integer arithmetic is used everywhere so results are exact (no float rounding errors).
"""

SAFE_BUFFER = 5   # within this many percentage points above T is a WARNING


def percentage(attended, total):
    return 0.0 if total == 0 else attended / total * 100


def meets(attended, total, threshold):
    """True if attended/total >= threshold%."""
    return attended * 100 >= threshold * total


def classes_can_skip(attended, total, threshold):
    """Max number of consecutive classes you can miss and still meet the threshold."""
    return max(0, (attended * 100) // threshold - total)


def classes_needed(attended, total, threshold):
    """Min consecutive classes to attend to reach the threshold.
    Returns 0 if already fine, or None if impossible (threshold 100% after any absence)."""
    if meets(attended, total, threshold):
        return 0
    if threshold >= 100:
        return None
    numerator = threshold * total - 100 * attended
    denominator = 100 - threshold
    return -(-numerator // denominator)      # ceiling division


def status(attended, total, threshold):
    """NO DATA / SAFE / WARNING / SHORTAGE."""
    if total == 0:
        return "NO DATA"
    if not meets(attended, total, threshold):
        return "SHORTAGE"
    if meets(attended, total, min(100, threshold + SAFE_BUFFER)):
        return "SAFE"
    return "WARNING"


def forecast(attended, total, remaining, planned_absences):
    """Final attendance % if you miss `planned_absences` of the `remaining` classes."""
    if planned_absences < 0 or planned_absences > remaining:
        raise ValueError("planned_absences must be between 0 and remaining")
    final_total = total + remaining
    final_attended = attended + remaining - planned_absences
    return percentage(final_attended, final_total)


def semester_outlook(attended, total, remaining, threshold):
    """How many of the remaining classes must be attended / can be missed.
    Returns dict with must_attend, can_miss, achievable."""
    final_total = total + remaining
    needed_attended = -(-(threshold * final_total) // 100)     # ceil(T*final/100)
    must_attend = max(0, needed_attended - attended)
    if must_attend > remaining:
        return {"must_attend": None, "can_miss": None, "achievable": False}
    return {"must_attend": must_attend, "can_miss": remaining - must_attend, "achievable": True}


def advice(attended, total, threshold):
    """One-line human-readable advice."""
    if total == 0:
        return "No classes recorded yet."
    if meets(attended, total, threshold):
        skip = classes_can_skip(attended, total, threshold)
        return f"You can skip {skip} more class(es)." if skip else "Do not skip - one miss drops you below."
    need = classes_needed(attended, total, threshold)
    if need is None:
        return "Cannot recover: 100% attendance is required."
    return f"Attend the next {need} class(es) in a row to reach {threshold}%."
