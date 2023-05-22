from docutils import nodes
from sphinx.application import Sphinx
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx_design.shared import is_component


class TeiElement(nodes.Element): pass

BASE_RULES = [
  {'selector': 'tei:body', 'tag': 'section'}
]

TAG_MAPPINGS = {
    '{http://www.tei-c.org/ns/1.0}body': 'section',
    '{http://www.tei-c.org/ns/1.0}head': 'h1',
    '{http://www.tei-c.org/ns/1.0}p': 'p',
    '{http://www.tei-c.org/ns/1.0}interp': 'aside',

    '{http://www.tei-c.org/ns/1.0}seg': 'span',
    '{http://www.tei-c.org/ns/1.0}pb': 'span',
    '{http://www.tei-c.org/ns/1.0}hi': 'span',
    '{http://www.tei-c.org/ns/1.0}ref': 'a',
    '{http://www.tei-c.org/ns/1.0}citedRange': 'span',
    '{http://www.tei-c.org/ns/1.0}q': 'span',
    '{http://www.tei-c.org/ns/1.0}hi': 'span',
    '{http://www.tei-c.org/ns/1.0}foreign': 'span',
    '{http://www.tei-c.org/ns/1.0}speaker': 'span',
    '{http://www.tei-c.org/ns/1.0}stage': 'span',
}

ATTRIBUTE_MAPPINGS = {
    '{http://www.tei-c.org/ns/1.0}ref': {
        'target': 'href',
    },
}


def tag_for_node(node: TeiElement) -> str:
    tei_tag = node.get('tei_tag')
    if tei_tag in TAG_MAPPINGS:
        return TAG_MAPPINGS[tei_tag]
    return 'div'


def tei_element_html_enter(self, node: TeiElement) -> None:
    tag = tag_for_node(node)
    if tag:
        buffer = [f'<{tag} data-tei-tag="{node.get("tei_tag")[29:]}"']
        if node.get('ids'):
            buffer.append(f' id="{node.get("ids")[0]}"')
        tei_tag = node.get('tei_tag')
        for key, value in node.get('tei_attributes').items():
            if tei_tag in ATTRIBUTE_MAPPINGS and key in ATTRIBUTE_MAPPINGS[tei_tag]:
                buffer.append(f' {ATTRIBUTE_MAPPINGS[tei_tag][key]}="{value}"')
            elif key == '{http://www.w3.org/XML/1998/namespace}id':
                buffer.append(f' id="{value}"')
            else:
                buffer.append(f' data-{key}="{value}"')
        self.body.append(f'{"".join(buffer)}>')


def tei_element_html_exit(self, node: TeiElement) -> None:
    tag = tag_for_node(node)
    if tag:
        self.body.append(f'</{tag}>')


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


def handle_config(app: Sphinx, config) -> None:
    print(config.uEdition)


def setup(app: Sphinx) -> None:
    app.add_post_transform(Tei2HtmlTransform)
    app.add_node(TeiElement, html=(tei_element_html_enter, tei_element_html_exit))
    app.add_config_value('uEdition', default=None, rebuild='html', types=[dict])
    app.connect('config-inited', handle_config)
    print(app.config)
