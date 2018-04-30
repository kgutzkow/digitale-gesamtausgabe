import click

@click.command()
@click.argument('input', type=click.File('r', encoding='iso-8859-1'))
@click.argument('output', type=click.File('w', encoding='utf-8'))
def convert(input, output):
    """Converts ISO-8859-1 input to UTF-8"""
    while True:
        chunk = input.read(4096)
        if not chunk:
            break
        output.write(chunk)

if __name__ == '__main__':
    convert()
