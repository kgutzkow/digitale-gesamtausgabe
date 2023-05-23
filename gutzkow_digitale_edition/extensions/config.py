from copy import deepcopy
from sphinx.application import Sphinx
from sphinx.config import Config


BASE_RULES = [
    {'selector': 'tei:body', 'tag': 'section'},
    {'selector': 'tei:head', 'tag': 'h1'},
    {'selector': 'tei:p', 'tag': 'p'},

    {'selector': 'tei:seg', 'tag': 'span'},
    {'selector': 'tei:pb', 'tag': 'span'},
    {'selector': 'tei:hi', 'tag': 'span'},
    {
        'selector': 'tei:ref',
        'tag': 'a',
        'attributes': [
            {'attr': 'href', 'source': 'target'}
        ]
    },
    {'selector': 'tei:citedRange', 'tag': 'span'},
    {'selector': 'tei:q', 'tag': 'span'},
    {'selector': 'tei:hi', 'tag': 'span'},
    {'selector': 'tei:foreign', 'tag': 'span'},
    {'selector': 'tei:speaker', 'tag': 'span'},
    {'selector': 'tei:stage', 'tag': 'span'},
    {'selector': 'tei:lem', 'tag': 'span'},
    {'selector': 'tei:sic', 'tag': 'span'},
]
_rules = []


def rules() -> list[dict]:
    return _rules


def fix_rules(rules: list[dict]) -> list[dict]:
    for rule in rules:
        if isinstance(rule['selector'], str):
            rule['selector'] = {'tag': rule['selector']}
        if 'attributes' in rule['selector'] and isinstance(rule['selector']['attributes'], dict):
            rule['selector']['attributes'] = [rule['selector']['attributes']]
        rule['selector']['tag'] = rule['selector']['tag'].replace('tei:', '{http://www.tei-c.org/ns/1.0}')
    return rules


def handle_config(app: Sphinx, config: Config) -> None:
    global _rules
    if 'mappings' in config.uEdition:
        _rules = fix_rules(config.uEdition['mappings'] + BASE_RULES)
    else:
        _rules = fix_rules(deepcopy(BASE_RULES))
    if 'sections' in config.uEdition:
        for section in config.uEdition['sections']:
            if 'mappings' in section:
                section['mappings'] = fix_rules(section['mappings'] + _rules)
            else:
                section['mappings'] = deepcopy(_rules)


def setup(app: Sphinx) -> None:
    app.add_config_value('uEdition', default=None, rebuild='html', types=[dict])
    app.connect('config-inited', handle_config)
