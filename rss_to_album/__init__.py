#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'rss_to_album'

from telegram_util import AlbumResult as Result
import yaml
from bs4 import BeautifulSoup, NavigableString
import feedparser
from urllib.parse import unquote
import export_to_telegraph

with open('credential') as f:
    credential = yaml.load(f, Loader=yaml.FullLoader)
export_to_telegraph.token = credential['telegraph_token']

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
        if not item.get('src'):
            continue
        yield resolveImg(item['src'].replace('&amp;', '&'))

def get(rss_path):
    feed = feedparser.parse(rss_path)
    feed_entries = feed.entries
    for entry in feed.entries:
        soup = BeautifulSoup(entry.description or entry.summary, 'html.parser')
        result = Result()
        try:
            result.url = entry.link
        except:
            result.url = entry.links[0].href[:-4]
        if 'https://crossing.cw.com.tw/' in result.url:
            result.cap = export_to_telegraph.export('http://webcache.googleusercontent.com/search?q=cache:'+result.url, True, True, True, True)
            yield result
            continue
        result.cap_html_v2 = getCap(soup)
        if 'idaily/today' in rss_path:
            result.cap_html_v2 = '【%s】\n\n%s' % (entry.title, result.cap_html_v2.rsplit('摄影师', 1)[0])
        if 'rss/bingwallpaper' in rss_path:
            result.cap_html_v2 = entry.title.split('(©')[0]
        result.imgs = list(getImgs(soup))
        # TODO: support video
        yield result