from pydantic import BaseModel, validator, ValidationError
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.util import logging
from typing import Union, Literal


logger = logging.getLogger(__name__)


class RuleSelectorAttribute(BaseModel):

    attr: str
    value: str


class RuleSelector(BaseModel):

    tag: str
    attributes: list[RuleSelectorAttribute] = []

    @validator('tag', pre=True)
    def expand_tag_namespace(cls, v, values, **kwargs) -> str:
        return v.replace('tei:', '{http://www.tei-c.org/ns/1.0}')

    @validator('attributes', pre=True)
    def convert_dict_attributes_to_list(cls, v, values, **kwargs) -> list[dict]:
        if isinstance(v, dict):
            return [v]
        return v


class RuleText(BaseModel):

    action: Literal['from-attribute']
    attr: str


class RuleAttributeCopy(BaseModel):

    action: Literal['copy'] = 'copy'
    attr: str
    source: str


class RuleAttributeSet(BaseModel):

    action: Literal['set']
    attr: str
    value: str


class RuleAttributeDelete(BaseModel):

    action: Literal['delete']
    attr: str


class Rule(BaseModel):

    selector: RuleSelector
    tag: Union[str, None] = 'div'
    text: Union[RuleText, None] = None
    attributes: list[Union[RuleAttributeCopy, RuleAttributeSet, RuleAttributeDelete]] = []

    @validator('selector', pre=True)
    def convert_str_selector_to_dict(cls, v, values, **kwargs) -> dict:
        if isinstance(v, str):
            return {'tag': v}
        return v


class Section(BaseModel):

    title: str
    content: str
    mappings: list[Rule] = []


class Config(BaseModel):

    text_only_in_leaf_nodes: bool = False
    mappings: list[Rule] = []
    sections: list[Section] = []


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


def validate_config(app: Sphinx, config: Config) -> None:
    if 'sections' in config.uEdition and isinstance(config.uEdition['sections'], list):
        if 'mappings' in config.uEdition and isinstance(config.uEdition['mappings'], list):
            for section in config.uEdition['sections']:
                if 'mappings' in section and isinstance(section['mappings'], list):
                    section['mappings'] = section['mappings'] + config.uEdition['mappings'] + BASE_RULES
                else:
                    section['mappings'] = config.uEdition['mappings'] + BASE_RULES
    try:
        config.uEdition = Config(**config.uEdition).dict()
    except ValidationError as e:
        for error in e.errors():
            logger.error(' -> '.join([str(l) for l in error['loc']]))
            logger.error(f'  {error["msg"]}')
        raise Exception('uEdition Validation Failed')


def setup(app: Sphinx) -> None:
    app.add_config_value('uEdition', default=None, rebuild='html', types=[dict])
    app.connect('config-inited', validate_config)
