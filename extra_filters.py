import json

from hashlib import sha256
from pelican import signals


def hash_sha256(text):
    digest = sha256()
    digest.update(text.encode('utf-8'))
    return digest.hexdigest()


def install_extra_filters(generator):
    """Install the extra filters."""
    generator.env.filters['json'] = json.dumps
    generator.env.filters['sha256'] = hash_sha256


def register():
    """Register the extra filters"""
    signals.generator_init.connect(install_extra_filters)
