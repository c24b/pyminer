#!/usr/bin/env/python
# -*- coding: utf-8 -*-
import tweetstream

class TwitterStream(object):
	def __init__(self, user,password, query):
		self.User = user
		self.Password = password
		self.Query = query
	def Get_Stream(self):
		with tweetstream.FilterStream(self.User, self.Password, track=self.Query) as stream:
			for tweet in stream:
				print "Got interesting tweet:", tweet


#query = ["hellobank", "hello bank", "Hellobank","hellobank", "#hellobank"]	
query = ["lol", "lol"]
t = TwitterStream("c4barbes", "maxim82_", query)		
t.Get_Stream()
