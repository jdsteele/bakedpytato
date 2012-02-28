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

import logging
logger = logging.getLogger(__name__)

class BasePlugin(object):
	default_encoding = 'ISO-8859-1'

	def recode(self, data):
		for key in data.iterkeys():
			if (isinstance(data[key], basestring) and 
				not isinstance(data[key], unicode)
			):
				try:
					q = data[key].decode(self.default_encoding)
					data[key] = q
				except Exception:
					logger.exception("Failed to recode '%s' to unicode from '%s' : ", data[key], self.default_encoding )
		return data
