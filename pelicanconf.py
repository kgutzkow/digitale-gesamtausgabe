#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
from datetime import datetime

AUTHOR = 'Mark M Hall'
SITENAME = 'Karl Gutzkow'
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

DEFAULT_PAGINATION = 6

DISPLAY_CATEGORIES_ON_MENU = False

PLUGIN_PATHS = ['./']
PLUGINS = ['tei_reader',
           'pelican_page_order',
           'pelican_page_hierarchy']

STATIC_PATHS = ['pages']

THEME = './theme'

GENERATION_DATE = datetime.now()

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

TAXONOMY = (
    ('I. Erzählerische Werke', 'erzaehlerische-werke', (
        ('1. Briefe eines Narren an eine Närrin', 'briefe-eines-narren-an-eine-naerrin', ()),
        ('3. Novellen', 'novellen', (
            ('Erster Band', 'erster-band', ()),
            ('Zweiter Band', 'zweiter-band', ()),
        )),
        ('4. Wally die Zweiflerin', 'wally-die-zweiflerin', ()),
        ('7. Kleine erzählerische Werke I', 'kleine-erzaehlerische-werke-i', (
            ('Imagina Unruh', 'imagina-unruh', ()),
        )),
        ('10. Die Diakonissin', 'die-diakonissin', ()),
        ('11. Der Zauberer von Rom', 'der-zauberer-von-rom', (
            ('Erstes Buch', 'erstes-buch', ()),
            ('Zweites Buch', 'zweites-buch', ()),
            ('Drittes Buch', 'drittes-buch', ()),
            ('Viertes Buch', 'viertes-buch', ()),
            ('Fünftes Buch', 'fuenftest-buch', ()),
            ('Sechstes Buch', 'sechstes-buch', ()),
            ('Siebentes Buch', 'siebentes-buch', ()),
            ('Achtes Buch', 'achtes-buch', ()),
            ('Neuntes Buch', 'neuntes-buch', ()),
        )),
        ('17. Die neuen Serapionsbrüder', 'die-neuen-serapionsbrueder', (
            ('Erster Band', 'erster-band', ()),
            ('Zweiter Band', 'zweiter-band', ()),
            ('Dritter Band', 'dritter-band', ())
        ))
    )),
    ('II. Dramatische Werke', 'dramatische-werke', (
        ('1. Marino Falieri', 'marino-falieri', ()),
		('1. Hamlet in Wittenberg', 'hamlet-in-wittenberg', ()),
		('1. Nero', 'nero', ()),
		('1. König Saul', 'koenig-saul', ()),
		('2. Richard Savage. Oder: Der Sohn einer Mutter', 'richard-savage', ()),
		('2. Werner. Oder: Herz und Welt', 'werner', ()),
		('2. Die Gräfin Esther', 'die-graefin-esther', ()),
		('2. Patkul', 'patkul', ())
    )),
    ('III. Schriften zur Politik und Gesellschaft', 'schriften-zur-politik-und-gesellschaft', (
        ('3. Die Zeitgenossen', 'die-zeitgenossen', (
            ('Erster Band', 'erster-band', ()),
            ('Zweiter Band', 'zweiter-band', ()),
        )),
        ('Säkularbilder (1846)', 'saekularbilder-1846', (
            ('Vorwort', 'vorwort', ()),
        )),
        ('Säkularbilder (1875)', 'saekularbilder-1875', (
            ('Vorwort', 'vorwort', ()),
        )),
        ('6. Verstreute Schriften zur Geschichte und Politik', 'verstreute-schriften-zur-geschichte-und-politik', (
            ('Zur Arnim-Affaire', 'zur-arnim-affaire', ()),
        )),
        ('8. Zum Gesellschaftsleben - Skizzen und Zeitfragen', 'zum-gesellschaftsleben-skizzen-und-zeitfragen', (
            ('Studien über das Negligé', 'studien-ueber-das-neglige', ()),
			('Naturgeschichte der deutschen Kameele', 'naturgeschichte-der-deutschen-kameele', ()),
			('Eine Criminalerinnerung', 'eine-criminalerinnerung', ()),
			('Die zoologischen Gärten', 'die-zoologischen-gaerten', ()),
			('Der Papierkorb', 'der-papierkorb', ())
        ))
    ))
)
