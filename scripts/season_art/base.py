"""The contract between a season and the asset builders.

A season never edits the default drawing. It only returns extra layers, and the builders in
build_assets.py place them. A builder called without a season produces the default look exactly.
"""


class Layers:
    """Extra content for one asset. Every field is optional.

    sun          replaces the sun on the banner: (x, y, radius, core color, ring color)
    sun_details  a callable that receives the banner's background Grid, to add details on the sun
    ground       SVG drawn right after the background, behind everything else
    sky          SVG drawn after the clouds, in front of the sky
    front        SVG drawn last, on top of everything
    rider_extra  SVG drawn inside the riding cowboy, so it moves with the rider
    css          extra CSS (animations)
    text         replaces the footer text
    label        extra sentence for the accessible description
    draw         a callable that receives the poster's Grid, to add pixels to it
    headwear     a callable (r, p, cx) that replaces the cowboy hat in the poster's portrait
    rider_dy     pixels to move the footer rider down, so that headwear is never clipped by the top edge
    width, height, scale, body  only for the strip asset
    """

    def __init__(self, **kw):
        defaults = dict(sun=None, sun_details=None, ground="", sky="", front="", rider_extra="",
                        css="", text=None, label="", draw=None, headwear=None, rider_dy=0, width=0, height=0, scale=1, body="")
        unknown = set(kw) - set(defaults)
        if unknown:
            raise TypeError("unknown layer fields: %s" % sorted(unknown))
        defaults.update(kw)
        self.__dict__.update(defaults)


class Decor:
    """Base class of a season. A method returns None when the season does not decorate that asset."""

    id = None
    name = None

    def banner(self):
        return None

    def footer(self):
        return None

    def poster(self):
        return None

    def strip(self):
        return None
