import re
import sys

from lxml import etree
from os import walk, path


ns = {'tei': 'http://www.tei-c.org/ns/1.0',
      'gutz': 'https://gutzkow.de/ns/1.0',
      'xml': 'http://www.w3.org/XML/1998/namespace'}

def get_ancestors(node):
    if node.getparent() is not None:
        return [node.getparent()] + get_ancestors(node.getparent())
    else:
        return []


def check_creation_date(doc, errors):
    """Checks that the machine-readable creation date is valid."""
    date = doc.xpath('/tei:TEI/tei:teiHeader/tei:profileDesc/tei:creation/tei:date/@when', namespaces=ns)
    if len(date) == 0:
        errors.append('No creation date specified')
        return
    elif len(date) > 1:
        errors.append('More than one creation date specified')
        return
    date = str(date[0])
    match = re.fullmatch('[0-9]{4}(?:-([0-9]{2})(?:-([0-9]{2}))?)?', date)
    if not match:
        errors.append('Creation date invalid ({0})'.format(date))
    elif match.group(1) and match.group(1) not in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
        errors.append('Invalid creation month ({0})'.format(match.group(1), date))
    elif match.group(2) and not re.fullmatch('(0[1-9])|([12][0-9])|(3[01])', match.group(2)):
        errors.append('Invalid creation day ({0})'.format(match.group(2), date))


def check_reponsible_users(doc, errors):
    """Checks that the respStmt entries are valid."""
    respStmts = doc.xpath('/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:respStmt', namespaces=ns)
    if len(respStmts) == 0:
        errors.append('No respStmt entries found')
        return
    for idx, respStmt in enumerate(respStmts):
        if '{{{0}}}id'.format(ns['xml']) not in respStmt.attrib:
            errors.append('respStmt {0} is missing the xml:id attribute')
        else:
            id_value = respStmt.attrib['{{{0}}}id'.format(ns['xml'])]
            if not re.fullmatch('[a-zA-Z]+', id_value):
                errors.append('respStmt {0} has an invalid xml:id attribute value {1}'.format(idx + 1, id_value))
        resp = respStmt.xpath('tei:resp', namespaces=ns)
        if len(resp) == 0:
            errors.append('respStmt {0} is missing its resp entry'.format(idx + 1))
        else:
            for idx2, r in enumerate(resp):
                if not r.xpath('text()') or r.xpath('text()')[0].strip() == '':
                    errors.append('respStmt {0} resp {1} is empty'.format(idx + 1, idx2 + 1))
                elif not r.xpath('text()')[0].startswith('Herausgeber') and not r.xpath('text()')[0].startswith('Autor') and not r.xpath('text()')[0].startswith('Übersetzer') and r.xpath('text()')[0] != 'TEI Transfer' and r.xpath('text()')[0] != 'Mitarbeit' and r.xpath('text()')[0] != 'Apparat' and r.xpath('text()')[0] != 'Stellenerläuterungen':
                    errors.append('respStmt {0} resp {1} must be one of Herausgeber, Herausgeberin, Autor, Autorin, Übersetzer, Übersetzerin, TEI Transfer, Mitarbeit, Stellenerläuterungen, or Apparat.'.format(idx + 1, idx2 + 1))
        name = respStmt.xpath('tei:name', namespaces=ns)
        if len(name) == 0:
            errors.append('respStmt {0} is missing its name entry'.format(idx + 1))
        else:
            for idx2, n in enumerate(name):
                if not n.xpath('text()') or n.xpath('text()')[0].strip() == '':
                    errors.append('respStmt {0} name {1} is empty'.format(idx + 1, idx2 + 1))


def check_revision_descriptions(doc, errors):
    """Checks that the revision descriptions are valid and refer to a responsible person."""
    changes = doc.xpath('/tei:TEI/tei:teiHeader/tei:revisionDesc/tei:change', namespaces=ns)
    for idx, change in enumerate(changes):
        if not change.xpath('text()') or change.xpath('text()')[0].strip() == '':
            errors.append('The change {0} is missing a textual description'.format(idx + 1))
        else:
            match = re.fullmatch(r'([0-9]+\.[0-9]+)(?::(.*))?', change.text)
            if not match:
                errors.append('The change {0} does not follow the pattern Version[: Description]'.format(idx + 1))
        date = change.xpath('@when')
        if len(date) == 0:
            errors.append('The change {0} has no machine readable date'.format(idx + 1))
        else:
            date = str(date[0])
            if not re.fullmatch('[0-9]{4}(-[0-9]{2}(-[0-9]{2})?)?', date):
                errors.append('The change {0} has an invalid machine readable date ({1})'.format(idx + 1, date))
        who = change.xpath('@who')
        if len(who) == 0:
            errors.append('The change {0} is not linked to a respStmt'.format(idx + 1))
        else:
            ids = [w[1:] for w in who[0].split(' ')]
            for user_id in ids:
                resp = doc.xpath("/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:respStmt[@xml:id='{0}']".format(user_id), namespaces=ns)
                if not resp:
                    errors.append('Change {0} refers to a missing respStmt {1}'.format(idx + 1, user_id))


def check_page_number_markup(doc, errors):
    """Check that page numbers are correctly marked up."""
    markup = doc.xpath('//tei:pb', namespaces=ns)
    for pb in markup:
        if 'n' not in pb.attrib:
            if len(pb) == 0:
                errors.append('Page begin markup without page number attribute')
        else:
            if not re.fullmatch('[IVX0-9]+\\??', pb.attrib['n']):
                errors.append('Page begin markup with invalid page number {0}'.format(pb.attrib['n']))
    markup = doc.xpath('//tei:hi', namespaces=ns)
    for hi in markup:
        if 'style' in hi.attrib:
            styles = hi.attrib['style'].split(' ')
            if 'font-style-italic' in styles:
                text = hi.xpath('text()')
                if text and re.fullmatch('.*\[[IVX0-9]+\].*', text[0]):
                    errors.append('Page number marked up as italic highlight')


def check_footnotes(doc, errors):
    """Check that footnotes are valid."""
    markup = doc.xpath('//tei:ref[@type="footnote"]', namespaces=ns)
    for note in markup:
        if 'target' not in note.attrib:
            errors.append('Reference missing a target')
        elif not doc.xpath('//tei:note[@xml:id="{0}"]'.format(note.attrib['target'][1:]), namespaces=ns):
            errors.append('Reference to missing footnote {0}'.format(note.attrib['target']))
    markup = doc.xpath('//tei:note[@type="footnote"]', namespaces=ns)
    for note in markup:
        if len(note) == 0:
            errors.append('Empty footnote')


def check_source_lists(doc, errors):
    """Check that the source lists are valid."""
    markup = doc.xpath("//tei:list[@type='sources']", namespaces=ns)
    for list in markup:
        next_sibling = list.getnext()
        if next_sibling is not None:
            if next_sibling.tag == '{{{0}}}list'.format(ns['tei']):
                if 'type' in next_sibling.attrib and next_sibling.attrib['type'] == 'sources':
                    errors.append('Two source lists next to each other')
    markup = doc.xpath("//tei:list[@type='sources']/tei:item", namespaces=ns)
    for item in markup:
        if len(item) == 0:
            errors.append('Source item without any content')
        if 'data-source-id' not in item.attrib or item.attrib['data-source-id'].strip() == '':
            errors.append('Empty source identifier')


def check_readings(doc, errors):
    """Check all readings for validity."""
    markup = doc.xpath('//tei:rdg', namespaces=ns)
    for rdg in markup:
        text = rdg.xpath('text()')
        if not text or text[0].strip() == '':
            errors.append('Empty reading')
        if 'wit' not in rdg.attrib:
            errors.append('No witness specified in the reading')
        elif rdg.attrib['wit'].strip() == '' or rdg.attrib['wit'].strip() == '#':
            errors.append('Empty witness specified in the reading')
        elif not rdg.attrib['wit'].startswith('#'):
            errors.append('Witness does not specify an identifier')
        else:
            source = doc.xpath("//tei:list[@type='sources']/tei:item[@data-source-id='{0}']".format(rdg.attrib['wit'][1:]), namespaces=ns)
            if len(source) == 0:
                errors.append('Witness refering to a missing source ({0})'.format(rdg.attrib['wit'][1:]))


def check_editor_transition(doc, errors):
    """Check that no old formatting exists."""
    references = doc.xpath('//tei:ref', namespaces=ns)
    for ref in references:
        if 'type' not in ref.attrib and 'target' not in ref.attrib:
            errors.append('Reference without target found')
        else:
            if 'type' in ref.attrib and ref.attrib['type'] not in ('esv', 'footnote', 'external'):
                errors.append('Old reference found')
            if 'type' not in ref.attrib and ref.attrib['target'] != '#global':
                errors.append('Reference to unknown target')
    annotations = doc.xpath('//tei:interp', namespaces=ns)
    for annotation in annotations:
        if 'type' not in annotation.attrib or annotation.attrib['type'] not in ('esv', ):
            errors.append('Old annotation found')
    footnotes = doc.xpath('//tei:note[@type="footnote"]', namespaces=ns)
    for footnote in footnotes:
        if 'data-marker' in footnote.attrib:
            errors.append('Old footnote found')
    markup = doc.xpath('//tei:note[@type="footnote"]', namespaces=ns)
    for note in markup:
        if note.text and note.text.strip() != '':
            errors.append('Footnote with direct text')


def check_empty_text_nodes(doc, errors):
    """Check that there are no empty text content nodes."""
    def walk_tree(node):
        if len(node) > 0:
            for child in node:
                walk_tree(child)
        elif not node.text and not node.attrib:
            errors.append('Empty {0} tag'.format(node.tag[node.tag.find('}') + 1:]))
    text = doc.xpath('//tei:text', namespaces=ns)
    walk_tree(text)


def check_stage_instructions(doc, errors):
    for stage in doc.xpath('//tei:stage', namespaces=ns):
        if 'type' not in stage.attrib:
            errors.append('Stage instruction missing type')
        elif stage.attrib['type'] not in ['setting', 'entrance', 'exit', 'business', 'novelistic', 'delivery', 'modifier', 'location', 'mixed']:
            if len(''.join(stage.itertext())) > 20:
                errors.append('Stage instruction with invalid type {0} ({1}...)'.format(stage.attrib['type'], ''.join(stage.itertext())[:20]))
            else:
                errors.append('Stage instruction with invalid type {0} ({1})'.format(stage.attrib['type'], ''.join(stage.itertext())))


def check_speaker(doc, errors):
    for speaker in doc.xpath('//tei:body//tei:speaker', namespaces=ns):
        found = False
        for ancestor in get_ancestors(speaker):
            if ancestor.tag == '{http://www.tei-c.org/ns/1.0}sp':
                found = True
        if not found:
            errors.append('Speaker outside of spoken text ({0})'.format(speaker.text))


def check_list_items(doc, errors):
    for item in doc.xpath('//tei:item', namespaces=ns):
        ancestors = get_ancestors(item)
        if not ancestors or ancestors[0].tag != '{http://www.tei-c.org/ns/1.0}list':
            errors.append('List item outside of a list')


errors = []

for basepath, _, filenames in walk('content'):
    for filename in filenames:
        if filename.endswith('.tei'):
            fullpath = path.join(basepath, filename)
            file_errors = []
            try:
                doc = etree.parse(fullpath)
                check_creation_date(doc, file_errors)
                check_reponsible_users(doc, file_errors)
                check_revision_descriptions(doc, file_errors)
                check_page_number_markup(doc, file_errors)
                check_footnotes(doc, file_errors)
                check_source_lists(doc, file_errors)
                check_readings(doc, file_errors)
                check_editor_transition(doc, file_errors)
                check_empty_text_nodes(doc, file_errors)
                check_stage_instructions(doc, file_errors)
                check_speaker(doc, file_errors)
                check_list_items(doc, file_errors)
            except etree.XMLSyntaxError as e:
                file_errors.append(str(e))
            if file_errors:
                errors.append((fullpath, file_errors))

if errors:
    error_count = 0
    for filename, error_list in errors:
        print('-' * len(filename), file=sys.stderr)
        print(filename, file=sys.stderr)
        for error in error_list:
            print(error, file=sys.stderr)
            error_count = error_count + 1
    print()
    print('{0} errors in {1} files'.format(error_count, len(errors)))
    sys.exit(1)
