from docutils import nodes
from docutils.parsers.rst import Parser as RstParser
from lxml import etree
from sphinx.parsers import Parser as SphinxParser
from sphinx.util import logging
from sphinx_design.shared import create_component


logger = logging.getLogger(__name__)
namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}


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
                tab_item = create_component('tab-item', classes=['sd-tab-item'])
                tab_label = nodes.rubric(section['title'], nodes.Text(section['title']), classes=['sd-tab-label'])
                tab_item.append(tab_label)
                tab_content = create_component('tab-content', classes=['sd-tab-content', 'tei'])
                tab_item.append(tab_content)
                self._walk_tree(root.xpath(section['content'], namespaces=namespaces)[0], tab_content)
                tab_set.append(tab_item)
        doc_section.append(tab_set)
        document.append(doc_section)

    def _walk_tree(self: 'TEIParser', node: etree.Element, parent: nodes.Element) -> None:
        is_leaf = len(node) == 0
        text_only_in_leaf_nodes = self.config.uEdition['text_only_in_leaf_nodes'] \
            if 'text_only_in_leaf_nodes' in self.config.uEdition else False
        new_element = create_component(
            'tei-tag',
            rawtext='',
            tei_tag=node.tag,
            tei_attributes=dict(node.attrib),
        )
        parent.append(new_element)
        if node.text and (is_leaf or not text_only_in_leaf_nodes):
            new_element.append(nodes.Text(node.text))
        for child in node:
            self._walk_tree(child, new_element)
        if node.tail and not text_only_in_leaf_nodes:
            parent.append(nodes.Text(node.tail))
