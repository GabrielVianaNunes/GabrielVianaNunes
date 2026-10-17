"""Seasonal decorations. Each season is a module in this package with a DECOR object.

Seasons are discovered automatically, so adding one never means editing a shared list. Each DECOR
carries its season `id` (as in data/seasons.json) and a `status`:

  "draft"     a design waiting for the owner's approval. It can be previewed but is never built for the profile.
  "approved"  the owner approved it. The daily build uses it inside its window.

`status` is "draft" by default, so a new season cannot go live by accident: its build issue changes the
one word after the owner approves the design.
"""
import importlib
import pkgutil

from .base import Decor, Layers  # noqa: F401

_SKIP = {"base"}
_ALL = {}


def _load():
    if not _ALL:
        for info in pkgutil.iter_modules(__path__):
            if info.name in _SKIP:
                continue
            decor = importlib.import_module("season_art." + info.name).DECOR
            _ALL[decor.id] = decor
    return _ALL


def get(season_id, drafts=False):
    """The decoration for a season id, or None when the season has no approved art. With drafts=True designs that
    are still waiting for approval are included, for previews only."""
    decor = _load().get(season_id)
    if decor is None:
        return None
    return decor if (decor.status == "approved" or drafts) else None


def ids(status=None):
    """The season ids that have art, optionally only those with a given status."""
    return sorted(i for i, d in _load().items() if status is None or d.status == status)
