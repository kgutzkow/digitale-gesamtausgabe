import click

from lxml import html, etree

ns = etree.FunctionNamespace('http://gutzkow.de')

@ns
def trim_pagenumber(context, match):
    """Trim the wrapping text (which is just styling) from pagenumbers"""
    return [str(page_nr).strip()[1:-1] for page_nr in match]

def classify(url):
    """Classify a given URL"""
    if url.startswith('SterbecE.htm#ERL'):
        return 'annotation'
    elif url.startswith('SterbecE.htm#GLK'):
        return 'comment'
    elif '/GuLex/' in url:
        return 'lexicon'
    elif url.startswith('../Zg/Zg2E.htm') or url.startswith('../BrN/Nrb11_99.htm') or url.startswith('../Rue/RueVT.htm'):
        return 'crossref'
    elif url.startswith('SterbecE.htm#QUE'):
        return 'quelle'
    elif url.startswith('SterbecE.htm#ENT'):
        return 'entstehungsgeschichte'
    elif url.startswith('SterbecE.htm#DOKWIRK'):
        return 'rezeptionsgeschichte'
    elif url.startswith('SterbecT.htm#TEXT'):
        return 'text'
    elif '/Archiv/Quellen/' in url:
        return 'source-text'
    else:
        print(url)
        return 'unknown'

@ns
def trim_crossref(context, match):
    """Trim a cross-reference to the local id"""
    return [str(href)[str(href).index('#') + 1:] if '#' in str(href) else str(href) for href in match]

@ns
def classify_crossref(context, match):
    """Classify a cross-reference"""
    return [classify(v) for v in match]

sequence_numbers = {}
@ns
def sequence_nr(context, key):
    """Generate a unique sequence number"""
    if key not in sequence_numbers:
        sequence_numbers[key] = 0
    sequence_numbers[key] = sequence_numbers[key] + 1
    return sequence_numbers[key]

@ns
def filter_characters(context, text, characters):
    """Filter the given set of characters (and all spaces)"""
    return [t.strip(characters).strip() for t in text if t.strip(characters).strip()]

@ns
def non_empty(context, a, b):
    """Return ``a`` if it is non-empty, otherwise return ``b``"""
    return a if a else b

@click.command()
@click.argument('input')
@click.argument('transform')
@click.argument('output', type=click.File('wb'))
@click.option('--input-html', 'loader', flag_value='html')
@click.option('--input-xml', 'loader', flag_value='html', default=True)
@click.option('--xslt-param', 'params', type=(str, str), multiple=True)
def convert(input, transform, output, loader, params):
    """Runs an XSLT script on a HTML file."""
    if loader == 'html':
        doc = html.parse(input)
    elif loader == 'xml':
        doc = etree.parse(input)
    transformer = etree.XSLT(etree.parse(transform))
    transformer(doc, **dict(params)).write_output(output)

if __name__ == '__main__':
    convert()
