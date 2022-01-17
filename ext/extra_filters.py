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


def fancy_date(date):
    date = [part[1:] if part.startswith('0') else part for part in date.split('-')]
    if len(date) == 1:
        return date[0]
    elif len(date) == 2:
        return '{0}.{1}'.format(date[1], date[0])
    elif len(date) == 3:
        return '{0}.{1}.{2}'.format(date[2], date[1], date[0])
    return ''


def install_extra_filters(generator):
    """Install the extra filters."""
    generator.env.filters['json'] = json.dumps
    generator.env.filters['sha256'] = hash_sha256
    generator.env.filters['sgroupby'] = sgroupby
    generator.env.filters['fancy_date'] = fancy_date


def register():
    """Register the extra filters"""
    signals.generator_init.connect(install_extra_filters)
