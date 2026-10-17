"""Seasonal decorations. Each season is a module with a DECOR object, looked up by its id."""
import importlib

from .base import Decor, Layers  # noqa: F401

# season id (as in data/seasons.json) -> module name
MODULES = {
    "halloween": "halloween",
    "christmas": "christmas",
}


def get(season_id):
    """The decoration for a season id, or None when the season has no art yet."""
    name = MODULES.get(season_id)
    if not name:
        return None
    return importlib.import_module("season_art." + name).DECOR
