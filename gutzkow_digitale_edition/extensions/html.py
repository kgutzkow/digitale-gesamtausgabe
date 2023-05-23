from copy import deepcopy
from docutils import nodes
from sphinx.application import Sphinx
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx_design.shared import is_component


class TeiElement(nodes.Element): pass


def tei_element_html_enter(self, node: TeiElement) -> None:
    buffer = [f'<{node.get("html_tag")} data-tei-tag="{node.get("tei_tag")[29:]}"']
    if node.get('ids'):
        buffer.append(f' id="{node.get("ids")[0]}"')
    for key, value in node.get('tei_attributes').items():
        buffer.append(f' {key}="{value}"')
    self.body.append(f'{"".join(buffer)}>')


def tei_element_html_exit(self, node: TeiElement) -> None:
    self.body.append(f'</{node.get("html_tag")}>')


class Tei2HtmlTransform(SphinxPostTransform):
    """Transform TEI containers into the HTML specific AST structures."""

    default_priority = 198
    formats = ("html",)

    def run(self):
        """Run the transform"""
        document: nodes.document = self.document
        for node in document.findall(lambda node: is_component(node, "tei-tag")):
            tei_element = TeiElement(
                html_tag=node.get('html_tag'),
                tei_tag=node.get('tei_tag'),
                tei_attributes=node.get('tei_attributes')
            )
            tei_element += list(node)
            node.replace_self(tei_element)


def setup(app: Sphinx) -> None:
    app.add_post_transform(Tei2HtmlTransform)
    app.add_node(TeiElement, html=(tei_element_html_enter, tei_element_html_exit))
