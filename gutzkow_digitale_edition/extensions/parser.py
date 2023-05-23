from docutils import nodes
from docutils.parsers.rst import Parser as RstParser
from lxml import etree
from sphinx.parsers import Parser as SphinxParser
from sphinx.util import logging
from sphinx_design.shared import create_component


logger = logging.getLogger(__name__)
namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}


def rule_for_node(node: etree.Element, rules) -> dict:
    tei_tag = node.tag
    for rule in rules:
        if rule['selector']['tag'] == tei_tag:
            if 'attributes' in rule['selector']:
                attr_match = True
                for attr_rule in rule['selector']['attributes']:
                    if attr_rule['attr'] not in node.attrib or \
                            node.attrib[attr_rule['attr']] != attr_rule['value']:
                        attr_match = False
                        break
                if not attr_match:
                    continue
            return rule
    return None


class TEIParser(SphinxParser):
    '''Sphinx parser for Markedly Structured Text (MyST).'''

    supported: tuple[str, ...] = ('tei',)
    '''Aliases this parser supports.'''

    settings_spec = RstParser.settings_spec
    '''Runtime settings specification.

    Defines runtime settings and associated command-line options, as used by
    `docutils.frontend.OptionParser`.  This is a concatenation of tuples of:

    - Option group title (string or `None` which implies no group, just a list
      of single options).

    - Description (string or `None`).

    - A sequence of option tuples
    '''

    config_section = 'tei parser'
    config_section_dependencies = ('parsers',)
    translate_section_name = None

    def get_transforms(self):
        return super().get_transforms()

    def parse(self, inputstring: str, document: nodes.document) -> None:
        '''Parse source text.

        :param inputstring: The source string to parse
        :param document: The root docutils node to add AST elements to

        '''
        root = etree.fromstring(inputstring.encode('UTF-8'))
        title = root.xpath('string(/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title)', namespaces=namespaces)
        doc_section = nodes.section(ids=['document'])
        doc_title = nodes.title()
        doc_title.append(nodes.Text(title if title else '[Untitled]'))
        doc_section.append(doc_title)
        tab_set = create_component('tab-set', classes=['sd-tab-set'])
        if 'sections' in self.config.uEdition:
            for section in self.config.uEdition['sections']:
                source = root.xpath(section['content'], namespaces=namespaces)
                if len(source) > 0:
                    tab_item = create_component('tab-item', classes=['sd-tab-item'])
                    tab_label = nodes.rubric(section['title'], nodes.Text(section['title']), classes=['sd-tab-label'])
                    tab_item.append(tab_label)
                    tab_content = create_component('tab-content', classes=['sd-tab-content', 'tei', nodes.make_id(section['title'])])
                    tab_item.append(tab_content)
                    for child in source:
                        self._walk_tree(child, tab_content, section['mappings'])
                    tab_set.append(tab_item)
        doc_section.append(tab_set)
        document.append(doc_section)

    def _walk_tree(self: 'TEIParser', node: etree.Element, parent: nodes.Element, rules) -> None:
        is_leaf = len(node) == 0
        text_only_in_leaf_nodes = self.config.uEdition['text_only_in_leaf_nodes'] \
            if 'text_only_in_leaf_nodes' in self.config.uEdition else False
        attributes = {}
        rule = rule_for_node(node, rules)
        if rule is not None and 'text' in rule:
            if rule['text']['action'] == 'from-attribute' and rule['text']['attr'] in node.attrib:
                node.text = node.attrib[rule['text']['attr']]
        for key, value in node.attrib.items():
            if key == '{http://www.w3.org/XML/1998/namespace}id':
                key = 'id'
            if rule and 'attributes' in rule:
                processed = False
                for attr_rule in rule['attributes']:
                    if 'action' not in attr_rule or attr_rule['action'] == 'copy':
                        if key == attr_rule['source']:
                            attributes[attr_rule['attr']] = value
                    elif 'action' in attr_rule and attr_rule['action'] == 'delete':
                        if key == attr_rule['attr']:
                            processed = True
                    elif 'action' in attr_rule and attr_rule['action'] == 'set':
                        if key == attr_rule['attr']:
                            value = attr_rule['value']
                if not processed:
                    if key == 'id':
                        attributes['id'] = value
                    else:
                        attributes[f'data-{key}'] = value
            else:
                if key == 'id':
                    attributes['id'] = value
                else:
                    attributes[f'data-{key}'] = value
        new_element = create_component(
            'tei-tag',
            rawtext='',
            tei_tag=node.tag,
            tei_attributes=attributes,
        )
        parent.append(new_element)
        if node.text and (is_leaf or not text_only_in_leaf_nodes):
            new_element.append(nodes.Text(node.text))
        for child in node:
            self._walk_tree(child, new_element, rules)
        if node.tail and not text_only_in_leaf_nodes:
            parent.append(nodes.Text(node.tail))
