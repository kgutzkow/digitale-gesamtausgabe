import re
import sys

from lxml import etree
from os import walk, path


ns = {'tei': 'http://www.tei-c.org/ns/1.0',
      'gutz': 'https://gutzkow.de/ns/1.0',
      'xml': 'http://www.w3.org/XML/1998/namespace'}

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
    if not re.fullmatch('[0-9]{4}(-[0-9]{2}(-[0-9]{2})?)?', date):
        errors.append('Creation date invalid ({0})'.format(date))


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
            except etree.XMLSyntaxError as e:
                file_errors.append(str(e))
            if file_errors:
                errors.append((fullpath, file_errors))

if errors:
    for filename, error_list in errors:
        print('-' * len(filename), file=sys.stderr)
        print(filename, file=sys.stderr)
        for error in error_list:
            print(error, file=sys.stderr)
    sys.exit(1)
