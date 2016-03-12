#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Swasher'
SITENAME = u'Antiskleroz'
#SITEURL = 'http://antiskleroz.pp.ua'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Kiev'

DEFAULT_LANG = 'ru'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 15

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True


# Blogroll
LINKS =  (
            ('Archives', 'archives.html'),
            ('Rtorrent', 'ustanovka-i-nastroika-rtorrent-rutorrent.html'),
            ('Linux commands', 'linux-commands.html'),
         )

# Social widget
SOCIAL = (
            ('twitter', 'http://twitter.com/mr_swasher'),
            ('facebook', 'facebook.com/alexey.swasher'),
            ('vkontakte', 'http://vk.com/mr.swasher'),
            ('github', 'http://github.com/swasher'),
         )



DISQUS_SITENAME = "Antiskleroz"
DISQUS_SHORTNAME = "antiskleroz"

GOOGLE_ANALYTICS = 'UA-3525597-4'
GOOGLE_SEARCH_ID = '013151284164154536357:cc1m6ctrcro'

#THEME = "themes/flasky"
THEME = "themes/subtle"
#THEME = "themes/pelican-elegant"


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

#DIRECT_TEMPLATES = (('index', 'tags', 'categories', 'authors', 'archives', 'search'))
DIRECT_TEMPLATES = (('index', 'search'))

SLUGIFY_SOURCE = 'basename'
