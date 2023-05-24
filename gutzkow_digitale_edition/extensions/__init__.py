from sphinx.application import Sphinx

from . import config, tei


def setup(app: Sphinx):
    """Setup the theme extensions."""
    config.setup(app)
    tei.setup(app)
    return {'parallel_read_safe': True, 'parallel_write_safe': True}
