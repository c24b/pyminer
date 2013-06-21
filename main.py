#!/usr/bin/env/python
# -*- coding: utf-8 -*-
import csv, re, json, os
from BeautifulSoup import BeautifulSoup
import urllib, urllib2
from multiprocessing import Pool
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

#import pdb; pdb.set_trace()
	
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
	def __init__(self, sourceType,name, url,value):
		self.SourceType = sourceType
		self.Name = name
		self.Url = url
		self.Value = value

class RessourceProvider:
	def __init__(self, filePath):
		self.FilePath = filePath
		
	def GetRessourceList(self):
		'''return a list of ressources'''
		result = []
		with open(self.FilePath, 'r') as f:
			reader = csv.reader(f, delimiter=",")
			for n in reader:
				try:
					result.append(Resource(n[0], n[1], n[2], n[::-1][0]))
				except IndexError:
					result.append(Resource(n[0], n[1], n[2], None))			
		return result

		
	def Update(self, newList):
		'''update a list of ressources'''
		rows = []
		f = open(self.FilePath, 'r')
		reader = csv.reader(f, delimiter=",")
		for row, i in zip(reader, newList):
			row.append(i[::-1][1])
			rows.append(row)
			#print rows
		f.close()
		f = open(self.FilePath, 'w')
		writer = csv.writer(f, delimiter=",")
		for r in rows:
			print r
			writer.writerow(r)
		f.close()
	
		
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
		video1 =  (raw.find("span", {"class": "watch-view-count "})).text
		value = re.sub(r"[^0-9]","", video1)
		return int(value)

class InstagramScraper(GenericScraper):
	def __init__(self, pageUrl):
		GenericScraper.__init__(self, pageUrl)
				
	def Scrap(self):
		raw = self.Fetch()	
		value =  raw.findAll("span", {"class": "chiffre"})[1].text
		return value

def ResultbySourcetype(liste, filtr):
	return [n[1:] for n in liste if n[0] == str(filtr)]

def calc(new, old):
	new = re.sub(r"[^0-9]","", str(new))	
	old = re.sub(r"[^0-9]","", str(old))
	try:
		calcul = int(new)-int(old)
		if calcul < 0:
			return str(calcul)
		elif calcul == 0:
			return "="
		else:
			return "+"+str(calcul)
	except ValueError:
		if new is None:
			return "Err"
		elif old is None:
			return "+"+str(new)
	
def get_data(res):
	'''return the value ressources'''	
	scrapper = None
	if res.SourceType == SourceType.Facebook:
		scrapper = FacebookScraper(res.Url)
		
	elif res.SourceType == SourceType.Twitter:
		scrapper = TwitterScraper(res.Url)
			
	elif res.SourceType == SourceType.Youtube:
		scrapper = YoutubeScraper(res.Url)
		
	elif res.SourceType == SourceType.Instagram:
		scrapper = InstagramScraper(res.Url)

	value = scrapper.Scrap()
	diff = calc(value, res.Value)
	return [res.SourceType,res.Name,value,diff]

def ordered(result):
	facebook = []
	twitter = []
	youtube = []
	instagram = []
	for n in result:
		if n[0] == "facebook":
			print n
			facebook.append(n)
		elif n[0] == "twitter":
			twitter.append(n)
		elif n[0] == "youtube":
			youtube.append(n)
		elif n[0] == "instagram":
			instagram.append(n)
		else:
			pass
	return [facebook, twitter, youtube, instagram] 
	
class Template():
	def __init__(self, results):
		now = datetime.now()
		self.Date = now.strftime("%d Juin %Y %H:%M")
		self.Title = "Bilan veille Hello bank! du %s" %(now.strftime("%d Juin %Y %H:%M"))
		self.Results = results
	def Generate(self):
		results = ordered(self.Results)
		THIS_DIR = os.path.dirname(os.path.abspath(__file__))
		j2_env = Environment(loader=FileSystemLoader(THIS_DIR),trim_blocks=True)
		return j2_env.get_template('templatetest.html').render(title=self.Title, date=self.Date, facebook=results[0], twitter=results[1],youtube=results[2], intagram=results[3])

def Send(date, message):
		html = msg.encode('utf-8')
		text = ''
		subject = "Bilan Hello Bank! du %s" %date
		message = createhtmlmail(html, text, subject, 'From Constance')
		server = smtplib.SMTP("smtp.gmail.com","587")
		# Credentials (if needed)
		username = 'labomatixxx'
		password = 'Lavagea70degres'
		# The actual mail send
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		server.login(username,password)
		server.sendmail('labomatixxx@gmail.com', 'constance@comptoirsdumultimedia.com', message)
		server.quit()
		return 'ok'
	
	
if __name__=="__main__":
	resProvider = RessourceProvider('ressource.csv')
	resources = resProvider.GetRessourceList()
	p = Pool(5)
	result = p.map(get_data, resources)
	mail = Template(result)
	n = mail.Generate()
	
	
