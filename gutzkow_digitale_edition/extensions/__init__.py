from sphinx.application import Sphinx

from docutils import nodes
from sphinx.util.docutils import SphinxDirective
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx_design.shared import is_component, create_component


def setup(app):
    """Setup the theme extensions."""
    return {'parallel_read_safe': True, 'parallel_write_safe': True}
