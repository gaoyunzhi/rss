#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'rss_to_album'

from telegram_util import AlbumResult as Result
import yaml
from bs4 import BeautifulSoup, NavigableString
import feedparser
from urllib.parse import unquote

def getCap(soup):
    result = []
    for item in soup:
        if isinstance(item, NavigableString):
            text = item.strip()
            pieces = text.split()
            if pieces and pieces[0].startswith('@'):
                text = text.replace(pieces[0], '')
            if pieces and pieces[-1].startswith('@'):
                text = text.replace(pieces[-1], '')
            result.append(text.strip())
        elif item.name == 'br':
            result.append('\n')
        elif item.name == 'div':
            result.append(item.text.strip() + '\n\n')
        elif item.name == 'a' and 'rss.app' == item.text:
            ...
        elif item.name not in ['img'] and '(Feed generated with FetchRSS)' != item.text:
            print(item.name, item.text.strip())
    return ''.join(result).strip()

def resolveImg(url):
    pivot = 'http://static.careerengine.us/api/aov2/'
    if not url.startswith(pivot):
        return url
    url = url.split(pivot)[1]
    url = unquote(url)
    return url.replace('_|_', '/')

def getImgs(soup):
    for item in soup.find_all('img'):
        yield resolveImg(item['src'].replace('&amp;', '&'))

def get(rss_path):
    feed = feedparser.parse(rss_path)
    with open('details_log', 'a') as f:
        f.write('%s\n%s\n\n' % (rss_path, str(feed)))
    feed_entries = feed.entries
    for entry in feed.entries:
        soup = BeautifulSoup(entry.description or entry.summary, 'html.parser')
        result = Result()
        result.url = entry.link
        result.cap_html_v2 = getCap(soup)
        result.imgs = list(getImgs(soup))
        # TODO: support video
        yield result