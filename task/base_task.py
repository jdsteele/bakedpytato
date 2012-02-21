# -*- coding: utf-8 -*-
"""
	BakedPotato — Inventory Management System

	BakedPotato IMS
	Copyright 2010-2012, John David Steele (john.david.steele@gmail.com)

	Licensed under The MIT License
	Redistributions of files must retain the above copyright notice.

	@copyright     Copyright 2010-2012, John David Steele (john.david.steele@gmail.com)
	@license       MIT License (http://www.opensource.org/licenses/mit-license.php)
"""
#Pragma
from __future__ import unicode_literals

from session import Session
import re
import ttystatus

class BaseTask(object):
	logref = None

	def term_stat(self, message, count=None):
		ts = ttystatus.TerminalStatus(period=0.5)
		ts.add(ttystatus.Literal("{:^64} ".format(message)))
		ts.add(ttystatus.Literal(' Elapsed: '))
		ts.add(ttystatus.ElapsedTime())
		ts.add(ttystatus.Literal(' Remaining: '))
		ts.add(ttystatus.RemainingTime('done', 'total'))
		ts.add(ttystatus.Literal(' '))
		ts.add(ttystatus.PercentDone('done', 'total', decimals=2))
		ts.add(ttystatus.Literal(' '))
		ts.add(ttystatus.Integer('done'))
		ts.add(ttystatus.Literal(' of '))
		ts.add(ttystatus.Integer('total'))
		ts.add(ttystatus.Literal('  Sub: '))
		ts.add(ttystatus.PercentDone('sub_done', 'sub_total', decimals=2))
		ts.add(ttystatus.Literal(' '))
		ts.add(ttystatus.Integer('sub_done'))
		ts.add(ttystatus.Literal(' of '))
		ts.add(ttystatus.Integer('sub_total'))
		ts.add(ttystatus.Literal("      \r"))
		if count is not None:
			ts['total'] = count
		ts['done'] = 0
		ts['sub_done'] = 0
		return ts
	
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

