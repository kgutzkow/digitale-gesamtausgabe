#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from datetime import datetime

AUTHOR = 'Mark M Hall'
SITENAME = 'Karl Gutzkow - Digitale Gesamtausgabe'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Berlin'

DEFAULT_LANG = 'de'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('eHumanities@Martin-Luther-Universität Halle-Wittenberg', 'https://blogs.urz.uni-halle.de/ehumanities/'),)

DEFAULT_PAGINATION = 10

PLUGIN_PATHS = ['./']
PLUGINS = ['tei_reader',
           'pelican_page_hierarchy',
           'pelican_page_order']

THEME = './theme'

GENERATION_DATE = datetime.now()

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
