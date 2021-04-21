#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import praw
from telegram_util import log_on_fail
from telegram.ext import Updater
import plain_db
import cached_url
from bs4 import BeautifulSoup
import album_sender
import time

with open('credential') as f:
	credential = yaml.load(f, Loader=yaml.FullLoader)

with open('db/setting') as f:
	setting = yaml.load(f, Loader=yaml.FullLoader)

existing = plain_db.loadKeyOnlyDB('existing')
tele = Updater(credential['bot_token'], use_context=True)
debug_group = tele.bot.get_chat(credential['debug_group'])

@log_on_fail(debug_group)
def run():
	for channel_id, detail in setting.items():
		channel = tele.bot.get_chat(channel_id)
		for name, rss in detail.items():
			


if __name__ == '__main__':
	run()