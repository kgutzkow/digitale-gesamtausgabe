import os

from pelican import signals


def write_tei(generator, content):
    """Copy the source TEI to the output path."""
    if content.source_path.endswith('.tei'):
        output_filename = os.path.join(generator.output_path, f'{content.save_as[:-5]}.tei')
        os.makedirs(os.path.dirname(output_filename), exist_ok=True)
        with open(content.source_path) as in_f, open(output_filename, 'w') as out_f:
            out_f.write(in_f.read())


def register():
    """Register the static tei copying"""
    signals.page_generator_write_page.connect(write_tei)
