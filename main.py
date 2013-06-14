#!/usr/bin/env/python
# -*- coding: utf-8 -*-
import csv, re, json
from BeautifulSoup import BeautifulSoup
import urllib, urllib2
from multiprocessing import Pool

class SourceType:
	'''define the SourceType'''
	Undefined = ""
	Twitter = "twitter"
	Facebook = "facebook"
	Instagram = "instagram"
	Youtube = "youtube"
	GooglePlus= "googleplus"
	Pinterest = "pinterest"
	
class Resource:
	'''define the ressource composed by an url a sourcetype and a name'''
	def __init__(self, sourceType,name, url):
		self.SourceType = sourceType
		self.Name = name
		self.Url = url

class RessourceProvider:
	'''return a list of ressources'''
	def __init__(self,filePath):
		self.FilePath = filePath
	def GetRessourceList(self):
		result = []
		with open(self.FilePath, 'r') as f:
			reader = csv.reader(f, delimiter=",")
			for n in reader:
				try:
					result.append(Resource(n[0], n[1], n[2]))
				except IndexError:
					pass
		return result

class GenericScraper:
	'''return an object BeautifulSoup'''
	def __init__(self,pageurl):
		self.PageUrl = pageurl
		
	def Fetch(self):
		doc = urllib.urlopen(self.PageUrl)
		html = doc.read()
		doc.close()
		raw = BeautifulSoup(html)
		return raw
		
class FacebookScraper(GenericScraper):
	def __init__(self, pageUrl):
		GenericScraper.__init__(self, pageUrl)
				
	def Scrap(self):
		raw = self.Fetch()
		n = raw.findAll('code')
		if n is not None:
			res = (n[2].string).encode("utf-8")
			like = re.split("fcg.>|J\’aime", res)
			value = re.sub(ur"[^0-9]","", like[2])
			return value
			
class TwitterScraper(GenericScraper):
	def __init__(self, pageUrl):
		GenericScraper.__init__(self, pageUrl)
				
	def Scrap(self):
		raw = self.Fetch()
		res = raw.find('input', {'class':'json-data'})
		try:
			data = json.loads(res['value'])
			value = data['profile_user']['followers_count']
			return value
		except TypeError:
			pass
		
class YoutubeScraper(GenericScraper):
	def __init__(self, pageUrl):
		GenericScraper.__init__(self, pageUrl)
				
	def Scrap(self):
		raw = self.Fetch()	
		video1 =  raw.find("span", {"class": "watch-view-count "}).text
		value = re.sub(ur"[^0-9]","",video1)
		return value

class InstagramScraper(GenericScraper):
	def __init__(self, pageUrl):
		GenericScraper.__init__(self, pageUrl)
				
	def Scrap(self):
		raw = self.Fetch()	
		value =  raw.findAll("span", {"class": "chiffre"})[1].text
		return value

#~ class RessourceProvider:
	#~ '''return a list of ressources'''
	#~ def __init__(self,resource):
		#~ self.Ressource = ressource
	#~ 
	#~ def GetRessource(self):
		#~ d = {}
		#~ scrapper = None
		#~ if res.SourceType == SourceType.Facebook:
			#~ scrapper = FacebookScraper(res.Url)
			#~ value = scrapper.Scrap()
			#~ d[res.SourceType] = (res.Name, value)
		#~ elif res.SourceType == SourceType.Twitter:
			#~ scrapper = TwitterScraper(res.Url)
			#~ value = scrapper.Scrap()
			#~ d[res.SourceType] = (res.Name, value)
		#~ elif res.SourceType == SourceType.Youtube:
			#~ scrapper = YoutubeScraper(res.Url)
			#~ value = scrapper.Scrap()
			#~ d[res.SourceType] = (res.Name, value)
		#~ elif res.SourceType == SourceType.Instagram:
			#~ scrapper = InstagramScraper(res.Url)
			#~ value = scrapper.Scrap()
			#~ d[res.SourceType] = (res.Name, value)
		#~ else:
			#~ return 'Unhandled'
		#~ return d
			#~ 
	  
	
def ResultProvider(res):
	'''return the value ressources'''
	d = {}
	scrapper = None
	if res.SourceType == SourceType.Facebook:
		scrapper = FacebookScraper(res.Url)
		value = scrapper.Scrap()
		d['name'] = res.Name
		d['sourcetype']= res.SourceType
		d['value'] = value
		
	elif res.SourceType == SourceType.Twitter:
		scrapper = TwitterScraper(res.Url)
		value = scrapper.Scrap()
		d['name'] = res.Name
		d['sourcetype']= res.SourceType
		d['value'] = value
		
	elif res.SourceType == SourceType.Youtube:
		scrapper = YoutubeScraper(res.Url)
		value = scrapper.Scrap()
		d['name'] = res.Name
		d['sourcetype']= res.SourceType
		d['value'] = value
		

	elif res.SourceType == SourceType.Instagram:
		scrapper = InstagramScraper(res.Url)
		value = scrapper.Scrap()
		d['name'] = res.Name
		d['sourcetype']= res.SourceType
		d['value'] = value
			
	else:
		return 'Unhandled'
	return d

#~ class DataLibrary():
	#~ def __init__(self, pageUrl):
		#~ Resource.__init__(self)
		#~ value = 
	
#~ Class DataProvider():
	#~ def __init__(self, pageUrl):
	#~ if res.SourceType == SourceType.Facebook:
		#~ Facebook.append(ResultProvider(res))
					
if __name__=="__main__":
	resProvider = RessourceProvider('ressource.csv')
	resources = resProvider.GetRessourceList()
	p = Pool(5)
	result = p.map(ResultProvider, resources)
	print result
