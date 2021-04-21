#!/usr/bin/env python3
# -*- coding: utf-8 -*-

name = 'rss_to_album'

from telegram_util import AlbumResult as Result
import yaml
import cached_url
from bs4 import BeautifulSoup
import feedparser

def getCap(soup):
    

def getImgs(soup):
    for item in soup.find_all('img'):
        yield item['src'].replace('&amp;', '&') 

def get(rss_path):
    feed = feedparser.parse(rss_path)
    feed_entries = feed.entries
    for entry in feed.entries:
        soup = BeautifulSoup(entry.description, 'html.parser')
        result = Result()
        result.url = entry.link
        result.cap = getCap(soup)
        result.imgs = list(getImgs(soup))
        # TODO: support video
        yield result