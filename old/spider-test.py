import urllib2
from selenium import webdriver  
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys  
import re
from bs4 import BeautifulSoup
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
# url = 'http://www.washingtonpost.com/pb/newssearch/?query=politics&contenttype=Article%2CBlog%2C&searchType=&blogName=&datefilter=All+Since+2005&sort=Relevance&startat=9120'
url = 'http://news.ifeng.com/listpage/4550/20140701/2/rtlist.shtml'
try:
	req = urllib2.Request(url= url,headers = headers)
	result = urllib2.urlopen(req)
except Exception,e:
	print e
else:
# browser = webdriver.Firefox()  
# browser.get(url)  
# html_source = browser.page_source 
# browser.quit()

soup = BeautifulSoup(result)  

def openUrl(self,url):
	pass
def getUrl(self,url):
	for html in soup.select(".newsList"):
		for tag_ul in html.find_all('ul'):
			for tag_li in tag_ul.find_all('li'):
				print tag_li.find('a').get('href')
def getPage(self,url):
	pass
# 	print 
	# print html.a.get('href')

# print soup.title.string
# print soup.p.get_text().encode('utf-8')


