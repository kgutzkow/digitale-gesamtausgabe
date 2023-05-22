from copy import deepcopy
from docutils import nodes
from sphinx.application import Sphinx
from sphinx.transforms.post_transforms import SphinxPostTransform
from sphinx_design.shared import is_component


class TeiElement(nodes.Element): pass

BASE_RULES = [
    {'selector': 'tei:body', 'tag': 'section'},
    {'selector': 'tei:head', 'tag': 'h1'},
    {'selector': 'tei:p', 'tag': 'p'},

    {'selector': 'tei:seg', 'tag': 'span'},
    {'selector': 'tei:pb', 'tag': 'pb'},
    {'selector': 'tei:hi', 'tag': 'span'},
    {
        'selector': 'tei:ref',
        'tag': 'a',
        'attrs': [
            {'attr': 'href', 'source': 'target'}
        ]
    },
    {'selector': 'tei:citedRange', 'tag': 'span'},
    {'selector': 'tei:q', 'tag': 'span'},
    {'selector': 'tei:hi', 'tag': 'span'},
    {'selector': 'tei:foreign', 'tag': 'span'},
    {'selector': 'tei:speaker', 'tag': 'span'},
    {'selector': 'tei:stage', 'tag': 'span'},
    {'selector': 'tei:lem', 'tag': 'span'},
    {'selector': 'tei:sic', 'tag': 'span'},
]
rules = []

ATTRIBUTE_MAPPINGS = {
    '{http://www.tei-c.org/ns/1.0}ref': {
        'target': 'href',
    },
}


def tag_for_node(node: TeiElement) -> str:
    tei_tag = node.get('tei_tag')
    for rule in rules:
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
            return rule['tag']
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
    global rules
    if 'mappings' in config.uEdition:
        rules = config.uEdition['mappings'] + BASE_RULES
    else:
        rules = deepcopy(BASE_RULES)
    for rule in rules:
        if isinstance(rule['selector'], str):
            rule['selector'] = {'tag': rule['selector']}
        if 'attributes' in rule['selector'] and isinstance(rule['selector']['attributes'], dict):
            rule['selector']['attributes'] = [rule['selector']['attributes']]
        rule['selector']['tag'] = rule['selector']['tag'].replace('tei:', '{http://www.tei-c.org/ns/1.0}')


def setup(app: Sphinx) -> None:
    app.add_post_transform(Tei2HtmlTransform)
    app.add_node(TeiElement, html=(tei_element_html_enter, tei_element_html_exit))
    app.add_config_value('uEdition', default=None, rebuild='html', types=[dict])
    app.connect('config-inited', handle_config)
