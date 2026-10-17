"""Seasonal decorations. Each season is a module with a DECOR object, looked up by its id.

Two registries keep an unapproved design from going live by accident:
  MODULES        seasons whose design the owner approved. Only these are used by the daily build.
  DRAFT_MODULES  designs waiting for approval. They can be previewed but are never built for the profile.
A season moves from DRAFT_MODULES to MODULES in its build issue, after the approval.
"""
import importlib

from .base import Decor, Layers  # noqa: F401

# season id (as in data/seasons.json) -> module name
MODULES = {
    "halloween": "halloween",
    "christmas": "christmas",
    "birthday": "birthday",
}
DRAFT_MODULES = {
    "new-year": "newyear",
}


def get(season_id, drafts=False):
    """The decoration for a season id, or None when the season has no approved art. With drafts=True
    designs that are still waiting for approval are included, for previews only."""
    name = MODULES.get(season_id) or (DRAFT_MODULES.get(season_id) if drafts else None)
    if not name:
        return None
    return importlib.import_module("season_art." + name).DECOR
