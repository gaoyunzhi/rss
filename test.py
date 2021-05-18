import feedparser
import yaml

with open('db/setting') as f:
	setting = yaml.load(f, Loader=yaml.FullLoader)

def test():
	for name, rss_path in setting.get(-1001402364957).items():
		key = rss_path.split('/')[-1].split('.')[0]
		freewechat_link = 'https://freewechat.com/profile/' + key
		feed = feedparser.parse(rss_path)
		subtitle = feed.feed.subtitle
		print('【%s】\n%s\nRss 链接: %s\n自由微信链接: %s\n\n' % (name, subtitle, rss_path, freewechat_link))

if __name__ == '__main__':
	test()