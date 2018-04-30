from lxml import html, etree

ns = etree.FunctionNamespace('http://gutzkow.de')

@ns
def trim_pagenumber(context, match):
    return [str(page_nr).strip()[1:-1] for page_nr in match]

@ns
def trim_crossref(context, match):
    return [str(href)[str(href).index('#') + 1:] for href in match]

doc = html.parse('text.html')
transformer = etree.XSLT(etree.parse('htmltext2tei.xslt'))

with open('text.tei', 'w') as out_f:
    print(transformer(doc), file=out_f)
