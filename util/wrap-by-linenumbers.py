import click

@click.command()
@click.argument('input')
@click.argument('output')
@click.option('--wrap', 'wraps', type=(int, int, str), multiple=True)
@click.option('--encoding', default='utf-8')
def convert(input, output, wraps, encoding):
    """Wraps a file by with div tags by line number (specified via the ``--wrap start end label`` parameter)."""
    wraps = list(wraps)
    wraps.sort()
    with open(input, encoding=encoding) as in_f:
        lines = in_f.readlines()
    with open(output, 'w', encoding=encoding) as out_f:
        for idx, line in enumerate(lines):
            idx = idx + 1
            for wrap in reversed(wraps):
                if idx == wrap[1]:
                    out_f.write('</div>\n')
            for wrap in wraps:
                if idx == wrap[0]:
                    out_f.write('<div data-processing="boundary" data-boundary="%s">\n' % wrap[2])
            out_f.write(line)

if __name__ == '__main__':
    convert()
