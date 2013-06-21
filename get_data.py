class Result(object):
	def __init__(self, ):
		RessourceProvider.__init__(self, )
		self.Value

class ResultProvider():
	def __init__(self, res):
		self.Data = res
		
	def Get_Data(self, res):
		'''return the value ressources'''
		d = {}
		scrapper = None
		if res.SourceType == SourceType.Facebook:
			scrapper = FacebookScraper(res.Url)
			value = scrapper.Scrap()
		
		elif res.SourceType == SourceType.Twitter:
			scrapper = TwitterScraper(res.Url)
			value = scrapper.Scrap()
			
		elif res.SourceType == SourceType.Youtube:
			scrapper = YoutubeScraper(res.Url)
			value = scrapper.Scrap()
			

		elif res.SourceType == SourceType.Instagram:
			scrapper = InstagramScraper(res.Url)
			value = scrapper.Scrap()
		self.Data = d 
		return json.dumps(self.Data)
