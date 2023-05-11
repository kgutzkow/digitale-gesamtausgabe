"""Gutzkow Digitale Gesamtausgabe Extensions."""
from sphinx.application import Sphinx

from . import extensions


def setup(app: Sphinx):
    """Setup the theme and its extensions."""
    extensions.setup(app)
