from session import Session
import re

class BaseTask(object):
	logref = None
	
	def __init__(self):
		"""Init"""
		self.session = Session(autocommit=True)
		
	def pluralize(self, word):
		if not word.endswith('s'):
			word = word + 's'
		return word

	def singularize(self, word):
		if word.endswith('s'):
			word.rtrim('s')
		return word

	def camel_case(self, words):
		output = ""
		for word in words.split("_"):
			if not word:
				output += "_"
				continue
			output += word.capitalize()
		return output
		
	def underscore(self, word):
		s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', word)
		return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

