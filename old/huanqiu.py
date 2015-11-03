import urllib2
from bs4 import BeautifulSoup
for num in range(1,11):
	url = "http://weapon.huanqiu.com/weaponlist/aircraft/list_1_0_0_0_%d"%num
	try:
		req=urllib2.Request(url= url)
		result = urllib2.urlopen(req)
		soup = BeautifulSoup(result)
		for div_name in soup.select(".name"):
			for tag_a in div_name.find_all("a"):
				print tag_a.get_text().encode('utf-8')
	except Exception,e:
		print e
	else:
		pass