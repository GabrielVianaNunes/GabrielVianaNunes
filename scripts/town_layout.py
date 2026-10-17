"""Turns weekly contribution totals into a street plan. Pure functions, no drawing.

Rules (docs/town/DESIGN.md, docs/wiki/Design-decisions.md):
  * one lot per week, oldest first, the older half on the back street, the newer on the front
  * the tier comes from the quartiles of the NON EMPTY weeks, so one huge week cannot flatten the rest
  * empty weeks become decorated empty lots, never gaps
  * unique buildings: sheriff office 1, bank 1, church up to 2 (the water tower is a landmark, not a lot)
  * everything else repeats on a fixed rotation, so the street never reshuffles from day to day
"""

MAX_LOTS = 60
EMPTY_DECOR = ("cactus", "post", "wagon", "barrels", "well")
TIER1 = ("cabin", "barn", "cabin", "stable", "cabin", "shack")
TIER2 = ("townhouse", "saloon", "store", "townhouse", "blacksmith")
# buildings without text on them can be mirrored for variety
MIRRORABLE = frozenset(["cabin", "barn", "stable", "shack", "townhouse", "church", "sheriff",
                        "blacksmith", "cactus", "post", "wagon", "barrels", "well"])


def thresholds(totals):
    """25th, 50th and 75th percentile of the non empty weeks (zeros if there are none)."""
    nz = sorted(t for t in totals if t > 0)
    if not nz:
        return (0, 0, 0)

    def q(p):
        return nz[min(len(nz) - 1, int(p * len(nz)))]

    return (q(0.25), q(0.5), q(0.75))


def tier_of(total, th):
    if total <= 0:
        return 0
    if total <= th[0]:
        return 1
    if total <= th[1]:
        return 2
    if total <= th[2]:
        return 3
    return 4


def assign_kinds(tiers):
    """Building kind for every lot, oldest first."""
    n = len(tiers)
    kinds = [""] * n
    for i, t in enumerate(tiers):
        if t == 0:
            kinds[i] = EMPTY_DECOR[i % len(EMPTY_DECOR)]
        elif t == 1:
            kinds[i] = TIER1[i % len(TIER1)]
        elif t == 2:
            kinds[i] = TIER2[i % len(TIER2)]
        elif t == 3:
            kinds[i] = "hotel"
        else:
            kinds[i] = "grand hotel"

    # bank: the most recent lot of the highest tier that has one (tier 4, else 3, else 2)
    for tier in (4, 3, 2):
        cand = [i for i, t in enumerate(tiers) if t == tier]
        if cand:
            kinds[cand[-1]] = "bank"
            break

    # churches: the two edges of town among the remaining hotels (one if there are fewer than 3)
    hotels = [i for i, k in enumerate(kinds) if k == "hotel"]
    if len(hotels) >= 3:
        kinds[hotels[0]] = "church"
        kinds[hotels[-1]] = "church"
    elif hotels:
        kinds[hotels[0]] = "church"

    # sheriff: closest to the middle among hotels, else among tier 2 houses and shops
    pool = [i for i, k in enumerate(kinds) if k == "hotel"]
    if not pool:
        pool = [i for i, t in enumerate(tiers) if t == 2 and kinds[i] != "bank"]
    if pool:
        kinds[min(pool, key=lambda i: (abs(i - n // 2), i))] = "sheriff"
    return kinds


def build_layout(weeks):
    """weeks: list of {"start": "YYYY-MM-DD", "total": int}, oldest first.

    Returns {"lots", "total", "peak", "current", "thresholds", "back_count"}.
    """
    weeks = list(weeks)[-MAX_LOTS:]
    totals = [w["total"] for w in weeks]
    th = thresholds(totals)
    tiers = [tier_of(t, th) for t in totals]
    kinds = assign_kinds(tiers)
    back_count = len(weeks) // 2
    lots = []
    for i, w in enumerate(weeks):
        row = "back" if i < back_count else "front"
        lots.append({
            "index": i,
            "start": w["start"],
            "total": w["total"],
            "tier": tiers[i],
            "kind": kinds[i],
            "row": row,
            "col": i if row == "back" else i - back_count,
            "mirror": bool(i % 2) and kinds[i] in MIRRORABLE,
        })
    peak = None
    if any(totals):
        best = max(totals)
        peak = max(i for i, t in enumerate(totals) if t == best)   # latest of the busiest weeks
    return {
        "lots": lots,
        "total": sum(totals),
        "peak": peak,
        "current": len(weeks) - 1 if weeks else None,
        "thresholds": th,
        "back_count": back_count,
    }
