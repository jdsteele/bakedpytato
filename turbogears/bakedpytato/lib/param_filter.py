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
from uuid import UUID
from decimal import Decimal

from formencode import validators
from formencode.api import is_validator

### Extended Library

### Application Library

### Module Globals

class ParamFilter(object):

	_data = dict()

	def __init__(self, params=dict(), meta=dict()):
		if not isinstance(meta, dict):
			raise TypeError("meta: expected a dict")

		for (key, val) in meta.iteritems():
			if val == 'uuid':
				meta[key] = UUID
			elif val == 'decimal':
				meta[key] = validators.Decimal
			elif val == 'bool':
				meta[key] = validators.StringBoolean
			elif val == 'int':
				meta[key] = validators.Int
			elif val == 'float':
				meta[key] = validators.Float


		if not isinstance(params, dict):
			raise TypeError("params: expected a dict")


		for (key, val) in params.iteritems():
			if val == '':
				params[key] = None
				continue
			if key in meta:
				m = meta[key]
				if is_validator(m):
					params[key] = m.to_python(val)
				elif type(m) == TypeType:
					params[key] = m(val)
				else:
					raise TypeError(type(m))
		self._data = params
	
	def __getitem__(self, key):
		result = None
		if key in self._data:
			result = self._data[key]
		print 'GET', key, result
		return result

	def __setitem__(self,key, value):
		self._data[key] = value
