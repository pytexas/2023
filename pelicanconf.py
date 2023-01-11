#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

from pelican.readers import HTMLReader
from pelican.settings import DEFAULT_CONFIG
from utils.filters import sidebar
from markdown.extensions.tables import TableExtension

from markdown.extensions.md_in_html import MarkdownInHtmlExtension
from markdown.extensions.attr_list import AttrListExtension


AUTHOR = "PyTexas Devs"
SITETITLE = "PyTexas 2023"
SITENAME = "PyTexas 2023"
SITESUBTITLE = "Home of Python in Texas"
SITEDESCRIPTION = "The PyTexas Foundation is a non-profit dedicated to educating engineers about Python in the state of Texas"
SITEURL = "http://localhost:8000"
SITESRC = "https://github.com/pytexas/conference.pytexas.org"
SITELOGO = SITEURL + "/static/favicon.png"
FAVICON = SITEURL + "/static/favicon.ico"

CONFERENCE_YEAR = 2023
CONFERENCE_DATES = "April 1 & 2, 2023"

PATH = "content/"

TIMEZONE = "America/Chicago"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# URL settings
# ARTICLE_URL = "{date:%Y}/{date:%m}/{date:%d}/{slug}/"
# ARTICLE_SAVE_AS = "{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html"
PAGE_URL = "{slug}/"
PAGE_SAVE_AS = "{slug}/index.html"
# DRAFT_URL = '{slug}.html'
# DRAFT_SAVE_AS = 'drafts/{slug}.html'

# Theme
THEME = "theme/pytexas-conf"

MARKDOWN = {
    "extensions": [
        TableExtension(),
        AttrListExtension(),
        MarkdownInHtmlExtension()
    ]
}

# Plugins
# PLUGIN_PATHS = ['pelican-plugins']
# PLUGINS = ['neighbors']

# static files
STATIC_PATHS = [
    "static",
    "favicon.ico"
]

JINJA_ENVIRONMENT = {
    "extensions": [
        "jinja2.ext.do"
    ]
}

COPYRIGHT_YEAR = 2022
COPYRIGHT_NAME = "PyTexas Foundation"

MAIN_MENU = True

DISPLAY_PAGES_ON_MENU = False

MENUITEMS = {
    "About": {
        "Index": "/about",
        "Pages": {
            "About PyTexas": "/about",
            "Code of Conduct": "/about/code-of-conduct",
            "Diversity Statement": "/about/diversity-statement",
            "Privacy Statement": "/about/privacy-statement",
            "Volunteering": "/about/volunteering",
            "FAQ": "/about/faq",
        },
        "Dropdown": True,
    },
    "Attend": {
        "Index": "/attend",
        "Pages": {
            "Buy Tickets": "https://ti.to/pytexas/2023",
            "Health and Safety Guidelines": "/attend/health",
            "Venue": "/attend/venue",
            "Parking": "/attend/parking",
            "Food": "/attend/food",
            "Grants": "/attend/grants",
        },
        "Dropdown": True,
    },
    "Sponsors": {
        "Index": "/sponsors",
        "Pages": {
            "Sponsors": "/sponsors/sponsors",
            "Why Sponsor": "/sponsors/why-sponsor",
            "Prospectus": "/sponsors/prospectus",
            
        },
        "Dropdown": True,
    },
    "Speaking": {
        "Index": "/speaking",
        "Dropdown": False,
    },
}

JINJA_FILTERS = {
    "sidebar": sidebar
}

# Blogroll
LINKS = {
    "PyCon": "https://pycon.org/",
    "Python.org": "https://www.python.org/"
}

# Social widget
SOCIAL = {
    "Twitter": "https://twitter.com/pytexas",
    "Discord": "https://discord.gg/jNPAbcNukj",
    "YouTube": "https://www.youtube.com/channel/UCkn0L-L6auy9YAmlSy9Kv1Q/playlists",
}

DEFAULT_PAGINATION = False
