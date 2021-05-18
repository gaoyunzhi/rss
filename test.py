with open('db/setting') as f:
	setting = yaml.load(f, Loader=yaml.FullLoader)

for name, rss_link in setting.get(-1001402364957).items():
	key = rss_link.split('/')[-1].split('.')[0]
	freewechat_link = 'https://freewechat.com/profile/' + key
	

