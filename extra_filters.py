import json

from hashlib import sha256
from jinja2.filters import environmentfilter, make_attrgetter
from pelican import signals


def hash_sha256(text):
    digest = sha256()
    digest.update(text.encode('utf-8'))
    return digest.hexdigest()


@environmentfilter
def sgroupby(environment, items, attribute):
    """Group-by filter that assumes that the items are already sorted."""
    attrgetter = make_attrgetter(environment, attribute)
    grouper = None
    tmp = []
    result = []
    for item in items:
        key = attrgetter(item)
        if key != grouper:
            if tmp:
                result.append((grouper, tmp))
            grouper = key
            tmp = [item]
        else:
            tmp.append(item)
    if tmp:
        result.append((grouper, tmp))
    return result


def install_extra_filters(generator):
    """Install the extra filters."""
    generator.env.filters['json'] = json.dumps
    generator.env.filters['sha256'] = hash_sha256
    generator.env.filters['sgroupby'] = sgroupby


def register():
    """Register the extra filters"""
    signals.generator_init.connect(install_extra_filters)
