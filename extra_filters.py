import json

from pelican import signals


def install_extra_filters(generator):
    """Install the extra filters."""
    generator.env.filters['json'] = json.dumps


def register():
    """Register the extra filters"""
    signals.generator_init.connect(install_extra_filters)
