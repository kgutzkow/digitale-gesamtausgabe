from sphinx.application import Sphinx

from docutils import nodes
from sphinx.util.docutils import SphinxDirective
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx_design.shared import is_component, create_component


SLIDESHOW_CODE = '''\
alert('Test');
'''


class SlideshowDirective(SphinxDirective):
    """The SlideshowDirective directive is used to generate an slideshow."""

    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        activity = create_component(
            'gutzkow-slideshow',
            rawtext=self.content
        )
        return [activity]


class SlideshowHtmlTransform(SphinxPostTransform):
    """Transform slideshow containers into the HTML specific AST structures."""

    default_priority = 198
    formats = ("html",)

    def run(self):
        """Run the transform"""
        document: nodes.document = self.document
        for node in document.findall(lambda node: is_component(node, "gutzkow-slideshow")):
            newnode = nodes.raw(rawsource=SLIDESHOW_CODE, classes='gutzkow-slideshow')
            node.replace_self(newnode)


def setup(app):
    """Setup the theme extensions."""
    app.add_directive('activity', SlideshowDirective)
    app.add_post_transform(SlideshowHtmlTransform)
    return {'parallel_read_safe': True, 'parallel_write_safe': True}
