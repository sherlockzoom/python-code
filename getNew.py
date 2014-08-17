import urllib2
from bs4 import BeautifulSoup
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
url = 'http://news.ifeng.com/listpage/4550/20140701/2/rtlist.shtml'
try:
    req = urllib2.Request(url= url,headers = headers)
    result = urllib2.urlopen(req)
except Exception,e:
    print e
else:
    soup = BeautifulSoup(result)  
    for html in soup.select(".newsList"):
        for tag_ul in html.find_all('ul'):
            for tag_li in tag_ul.find_all('li'):
                newsLink = tag_li.find('a').get('href')
                print newsLink

def openUrl(self,url):
    pass
def getUrl(self,url):
    pass
def getPage(self,url):
    pass


