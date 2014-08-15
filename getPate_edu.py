import urllib2
from selenium import webdriver  
# from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import os
import re
import math

num = 25031
count = 1
# os.mkdir('./Entertainment/comics')
os.chdir('./Local/education')
for count in range(4,80):
	print count
	url = "http://www.washingtonpost.com/pb/newssearch/?query=education&contenttype=&searchType=&blogName=&datefilter=All+Since+2005&sort=Relevance&startat=%d0"%count
	# def myParse(self,url,num=1):
	try:
		req=urllib2.Request(url= url)
		result = urllib2.urlopen(req)
	except Exception,e:
		print e
	else:
		# req = urllib2.Request(url= url)
		# result = urllib2.urlopen(req)  
		html = result.read()
		soup = BeautifulSoup(html)
		for tag_a in soup.find_all('h3'):
			filename = str(num) + '.txt'
			try:
				tag_a.a.get('href')
			except Exception,e:
				print e
			else:
				start_link = tag_a.a.get('href')
				if re.compile(r'http').match(start_link):
					pass
				else:
					start_link = ("http://www.washingtonpost.com" + start_link)
				fp = open(filename,'w')
				# fp.write(start_link + '\n')
				print(start_link)
				try:
					req = urllib2.Request(url= start_link)
				  	result = urllib2.urlopen(req)
				except Exception,e:
					print e
				else:
				  	html = result.read()
				  	soup = BeautifulSoup(html)
				  	try:
						title = soup.title.string.encode('utf-8')
					except Exception,e:
						print e
					else:
						# title = soup.title.string.encode('utf-8')
						# fp.write(title + '\n')
						print(title)
						if soup.article:
							fp.write(title + '\n')
							if soup.article.find_all('p'):
								for tag_p in soup.article.find_all('p'):
									 text = tag_p.get_text().encode('utf-8')
									 fp.write(text + '\n')
									 print(text)
							else:
								print("soup.article.find_all  not find")
								pass
						else:
							print("soup.article is error,continue to find next one")
							try:
								browser = webdriver.Firefox()  
								browser.get(url)  
								html_source = browser.page_source 
								browser.quit()
								soup = BeautifulSoup(html_source)
								if soup.article.find_all('p'):
									for tag_p in soup.article.find_all('p'):
										 text = tag_p.get_text().encode('utf-8')
										 fp.write(text + '\n')
										 print(text)
							except Exception,e:
								print e
							else:
								print("selenium not work !~~")
###############							
							# print soup
						fp.close()
						num += 1
# print(soup.title.string)


# print(soup.article.find_all('p').string).encode('utf-8')