#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals


# BASIC SETTINGS http://docs.getpelican.com/en/3.6.3/settings.html#basic-settings
############################################################################

AUTHOR = 'Swasher'
SITENAME = 'Antiskleroz'
#SITEURL = 'http://antiskleroz.pp.ua'
SITEURL = ''

CACHE_CONTENT = True
LOAD_CONTENT_CACHE = True
CHECK_MODIFIED_METHOD = 'mtime'
CONTENT_CACHING_LAYER = 'generator'

PATH = 'content'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

STATIC_PATHS = ['images',
                'extra',]

EXTRA_PATH_METADATA = {
    'extra/google4b275ebfe0f55969.html': {'path': 'google4b275ebfe0f55969.html' },
    'extra/.netlify': {'path': '.netlify'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
}


PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['lightbox',
           'liquid_tags.img',
           'liquid_tags.youtube',
           'tipue_search'
           ]

READERS = {'html': None}

DIRECT_TEMPLATES = ['index', 'search']

SLUGIFY_SOURCE = 'basename'


# URL SETTINGS  http://docs.getpelican.com/en/3.6.3/settings.html#url-settings
############################################################################

TIMEZONE = 'Europe/Kiev'


# FEED SETTINGS  http://docs.getpelican.com/en/3.6.3/settings.html#feed-settings
############################################################################

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


# PAGINATION  http://docs.getpelican.com/en/3.6.3/settings.html#pagination
############################################################################

DEFAULT_PAGINATION = 15


# TRANSLATIONS  http://docs.getpelican.com/en/3.6.3/settings.html#translations
############################################################################

DEFAULT_LANG = 'ru'

# THEMES SETTINGS  http://docs.getpelican.com/en/3.6.3/settings.html#themes
############################################################################

THEME = "themes/subtle"
# THEME = "themes/flasky"
# THEME = "themes/pelican-elegant"

DISQUS_SITENAME = "Antiskleroz"
DISQUS_SHORTNAME = "antiskleroz"

GOOGLE_ANALYTICS = 'UA-3525597-4'
GOOGLE_SEARCH_ID = '013151284164154536357:cc1m6ctrcro'

LINKS =  (
            ('Rtorrent', 'ustanovka-i-nastroika-rtorrent-rutorrent.html'),
            ('Linux commands', 'linux-commands.html'),
            ('Bacula', 'bacula.html'),
         )

SOCIAL = (
            ('twitter', 'http://twitter.com/mr_swasher'),
            ('facebook', 'facebook.com/alexey.swasher'),
            ('vkontakte', 'http://vk.com/mr.swasher'),
            ('github', 'http://github.com/swasher'),
         )
