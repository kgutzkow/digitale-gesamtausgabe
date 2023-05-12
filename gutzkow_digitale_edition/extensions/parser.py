from docutils import nodes
from docutils.parsers.rst import Parser as RstParser
from io import BytesIO
from lxml import etree
from sphinx.parsers import Parser as SphinxParser
from sphinx.util import logging


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
        self._walk_tree(root.xpath('/tei:TEI/tei:text/tei:body', namespaces=namespaces)[0], document)
        self._fix_sections(document)
        #main_section = self._parse_tei_header(root.xpath('/tei:TEI/tei:teiHeader', namespaces=namespaces)[0], document)
        #config: MdParserConfig = document.settings.env.myst_config

        # update the global config with the file-level config
        #try:
        #    topmatter = read_topmatter(inputstring)
        #except TopmatterReadError:
        #    pass  # this will be reported during the render
        #else:
        #    if topmatter:
        #        warning = lambda wtype, msg: create_warning(  # noqa: E731
        #            document, msg, wtype, line=1, append_to=document
        #        )
        #        config = merge_file_level(config, topmatter, warning)

    def _walk_tree(self: 'TEIParser', node: etree.Element, parent: nodes.Element) -> None:
        new_element = None
        if node.tag == '{http://www.tei-c.org/ns/1.0}body':
            new_element = parent
        elif node.tag == '{http://www.tei-c.org/ns/1.0}head':
            new_element = nodes.title()
            new_element['level'] = int(node.attrib['type'][6:])
            self._add_default_block_attributes(node, new_element)
            parent.append(new_element)
        elif node.tag == '{http://www.tei-c.org/ns/1.0}p':
            new_element = nodes.paragraph()
            self._add_default_block_attributes(node, new_element)
            parent.append(new_element)
        elif node.tag == '{http://www.tei-c.org/ns/1.0}sp':
            new_element = nodes.container()
            new_element.classes = ['spoken']
            self._add_default_block_attributes(node, new_element)
            parent.append(new_element)
        elif node.tag == '{http://www.tei-c.org/ns/1.0}lg':
            new_element = nodes.container()
            new_element.classes = ['line-group']
            self._add_default_block_attributes(node, new_element)
            parent.append(new_element)
        elif node.tag == '{http://www.tei-c.org/ns/1.0}l':
            new_element = nodes.container()
            new_element.classes = ['line']
            self._add_default_block_attributes(node, new_element)
            parent.append(new_element)
        elif node.tag == '{http://www.tei-c.org/ns/1.0}seg':
            new_element = nodes.Text(node.text)
            parent.append(new_element)
        elif node.tag == '{http://www.tei-c.org/ns/1.0}ref':
            new_element = nodes.reference(text=node.text)
            new_element['refuri'] = node.attrib['target']
            parent.append(new_element)
        elif node.tag == '{http://www.tei-c.org/ns/1.0}hi':
            if node.attrib['style'] == 'font-weight-bold':
                new_element = nodes.strong(text=node.text)
            elif node.attrib['style'] == 'font-style-italic':
                new_element = nodes.emphasis(text=node.text)
            elif node.attrib['style'] == 'letter-sparse':
                new_element = nodes.inline(text=node.text)
                new_element['classes'] = ['letter-sparse']
            elif node.attrib['style'] == 'font-size-small':
                new_element = nodes.inline(text=node.text)
                new_element['classes'] = ['font-size-small']
            else:
                print(node.attrib['style'])
            if new_element is not None:
                parent.append(new_element)
        elif node.tag == '{http://www.tei-c.org/ns/1.0}stage':
            new_element = nodes.inline(text=node.text)
            new_element['classes'] = ['stage', node.attrib['type']]
            parent.append(new_element)
        elif node.tag == '{http://www.tei-c.org/ns/1.0}speaker':
            new_element = nodes.inline(text=node.text)
            new_element['classes'] = ['speaker']
            parent.append(new_element)
        elif node.tag == '{http://www.tei-c.org/ns/1.0}foreign':
            new_element = nodes.inline(text=node.text)
            new_element['classes'] = ['foreign']
            parent.append(new_element)
        elif node.tag == '{http://www.tei-c.org/ns/1.0}pb':
            new_element = nodes.inline(text=node.attrib['n'])
            new_element['classes'] = ['page-begin']
            parent.append(new_element)
        else:
            print(node.tag)
        if new_element is not None:
            for child in node:
                self._walk_tree(child, new_element)

    def _fix_sections(self: 'TEIParser', document: nodes.document) -> None:
        sections = []
        stack = []
        for elem in document:
            if isinstance(elem, nodes.title):
                if elem['level'] == 1:
                    new_section = nodes.section()
                    new_section['ids'] = [nodes.make_id(elem.astext())]
                    new_section.append(elem)
                    sections.append(new_section)
                    stack = [(new_section, 1)]
                else:
                    if stack[-1][1] >= elem['level']:
                        stack.pop()
                    new_section = nodes.section()
                    new_section['ids'] = [nodes.make_id(elem.astext())]
                    new_section.append(elem)
                    stack[-1][0].append(new_section)
                    stack.append((new_section, elem['level']))
                del elem['level']
            else:
                stack[-1][0].append(elem)
        document.children = sections

    def _add_default_block_attributes(self: 'TEIParser', node: etree.Element, elem: nodes.Element) -> None:
        for attr in ['first-line-indent', 'margin-top', 'margin-right', 'margin-bottom', 'margin-left']:
            if attr in node.attrib:
                if 'classes' not in elem:
                    elem['classes'] = []
                repl = '\\.'
                elem['classes'].append(f'{attr}-{node.attrib[attr]}')