from sphinx.application import Sphinx

from .parser import TEIParser
from . import html

def setup(app: Sphinx):
    """Setup the theme extensions."""
    app.add_source_suffix('.tei', 'tei')
    app.add_source_parser(TEIParser)
    html.setup(app)
    return {'parallel_read_safe': True, 'parallel_write_safe': True}
