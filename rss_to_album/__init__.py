#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'rss_to_album'

from telegram_util import AlbumResult as Result
import yaml
import cached_url
from bs4 import BeautifulSoup
import feedparser

def getGallery(url):
    content = cached_url.get(url, force_cache=True)
    soup = BeautifulSoup(content, 'html.parser')
    for item in soup.find_all('a'):
        if item.parent.name != 'figure':
            continue
        yield item['href'] 

def get(rss_path):
    feed = feedparser.parse(rss_path)
    feed_entries = feed.entries
    for entry in feed.entries:
        print(entry.description)
        print(entry.link)
        result = Result()
        result.url = entry.link
        result.cap = ''
        result.imgs = []
        yield result