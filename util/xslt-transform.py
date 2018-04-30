import click

from lxml import html, etree

ns = etree.FunctionNamespace('http://gutzkow.de')

@ns
def trim_pagenumber(context, match):
    return [str(page_nr).strip()[1:-1] for page_nr in match]

@ns
def trim_crossref(context, match):
    return [str(href)[str(href).index('#') + 1:] for href in match]

@click.command()
@click.argument('input')
@click.argument('transform')
@click.argument('output', type=click.File('wb'))
@click.option('--input-html', 'loader', flag_value='html')
@click.option('--input-xml', 'loader', flag_value='html', default=True)
def convert(input, transform, output, loader):
    """Runs an XSLT script on a HTML file."""
    if loader == 'html':
        doc = html.parse(input)
    elif loader == 'xml':
        doc = etree.parse(input)
    transformer = etree.XSLT(etree.parse(transform))
    transformer(doc).write_output(output)

if __name__ == '__main__':
    convert()
