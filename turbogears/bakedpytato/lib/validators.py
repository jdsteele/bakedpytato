# -*- coding: utf-8 -*-
"""
	BakedPotato — Inventory Management System

	BakedPotato IMS
	Copyright 2010-2012, John David Steele (john.david.steele@gmail.com)

	Licensed under The MIT License
	Redistributions of files must retain the above copyright notice.

	@copyright	 Copyright 2010-2012, John David Steele (john.david.steele@gmail.com)
	@license	   MIT License (http://www.opensource.org/licenses/mit-license.php)
"""
### Pragma
from __future__ import unicode_literals

### Standard Library
import uuid

### Extended Library
from formencode.validators import *
from formencode.api import FancyValidator, Invalid

### Application Library

### Module Globals


class UUID(FancyValidator):
	def _to_python(self, value, state):
		
		if self.is_empty:
			if value == '':
				return is_empty
		try:
			return uuid.UUID(value)
		except:
			raise Invalid("Failed to convert value to UUID", value, state)

	def _from_python(self, value, state):
		try:
			return str(value)
		except:
			raise Invalid("Failed to convert value to string", value, state)
