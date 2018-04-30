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
def convert(input, transform, output):
    """Runs an XSLT script on a HTML file."""
    doc = html.parse(input)
    transformer = etree.XSLT(etree.parse(transform))
    transformer(doc).write_output(output)

if __name__ == '__main__':
    convert()
