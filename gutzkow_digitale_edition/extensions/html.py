from copy import deepcopy
from docutils import nodes
from sphinx.application import Sphinx
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx_design.shared import is_component

from .config import rules


class TeiElement(nodes.Element): pass


def rule_for_node(node: TeiElement) -> dict:
    tei_tag = node.get('tei_tag')
    for rule in rules():
        if rule['selector']['tag'] == tei_tag:
            if 'attributes' in rule['selector']:
                attr_match = True
                for attr_rule in rule['selector']['attributes']:
                    if attr_rule['attr'] not in node.get('tei_attributes') or \
                            node.get('tei_attributes')[attr_rule['attr']] != attr_rule['value']:
                        attr_match = False
                        break
                if not attr_match:
                    continue
            return rule
    return None


def tei_element_html_enter(self, node: TeiElement) -> None:
    rule = rule_for_node(node)
    if rule:
        tag = rule['tag']
    else:
        tag = 'div'
    if tag:
        buffer = [f'<{tag} data-tei-tag="{node.get("tei_tag")[29:]}"']
        if node.get('ids'):
            buffer.append(f' id="{node.get("ids")[0]}"')
        for key, value in node.get('tei_attributes').items():
            buffer.append(f' {key}="{value}"')
        self.body.append(f'{"".join(buffer)}>')


def tei_element_html_exit(self, node: TeiElement) -> None:
    rule = rule_for_node(node)
    if rule:
        self.body.append(f'</{rule["tag"]}>')
    else:
        self.body.append(f'</div>')


class Tei2HtmlTransform(SphinxPostTransform):
    """Transform TEI containers into the HTML specific AST structures."""

    default_priority = 198
    formats = ("html",)

    def run(self):
        """Run the transform"""
        document: nodes.document = self.document
        for node in document.findall(lambda node: is_component(node, "tei-tag")):
            tei_element = TeiElement(
                tei_tag=node.get('tei_tag'),
                tei_attributes=node.get('tei_attributes')
            )
            tei_element += list(node)
            node.replace_self(tei_element)


def setup(app: Sphinx) -> None:
    app.add_post_transform(Tei2HtmlTransform)
    app.add_node(TeiElement, html=(tei_element_html_enter, tei_element_html_exit))
