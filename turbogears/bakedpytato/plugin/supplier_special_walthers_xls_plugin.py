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
### Pragma
from __future__ import unicode_literals

### Standard Library
import calendar
import logging 
import re
import struct
import tempfile
from datetime import date, timedelta
from decimal import *

### Extended Library

### Application Library
from plugin.base_supplier_special_plugin import BaseSupplierSpecialPlugin

### Module Globals
logger = logging.getLogger(__name__)

### Classes

class SupplierSpecialWalthersXLSPlugin(BaseSupplierSpecialPlugin):
	
	patterns = [
		r'(\d.{13}) (.{30})(.{5})([\d. ]{8})([\d. ]{7})(\d{2}%)',
		r'(\d.{12}) (.{26})(.{8})([\d. ]{9})([\d. ]{7})(\d{2}%)' #from 20100301
	]

	def match_file_import(self, file_import):
		if re.search('lock', file_import.name):
			return False
		if not re.search(r'Sale_Flyer_orderform.xls', file_import.name):
			return False
		magic = file_import.magic()
		if magic['mime'] != 'application/vnd.ms-excel':
			return False
		return True

	def get_items(self, supplier_special):
		return
		content = supplier_special.file_import.content
		lines = re.split("\n", content)
		for row in lines:
			
			if row.startswith('MANU-ITEM'):
				continue
			if row.endswith('Hotlist'):
				continue
			
			if row == '':
				yield None
				continue
			data = dict()
			m = False
			for pattern in self.patterns:
				m = re.match(pattern, row)
				if m:
					break
			
			if m:
				data['MANU-ITEM'] = m.group(1).strip()
				data['DESCRIPTION'] = m.group(2).strip()
				data['SCALE'] = m.group(3).strip()
				data['RET'] = m.group(4).strip()
				data['DLR'] = m.group(5).strip()
				data['DISC'] = m.group(6).strip()
			else:
				logger.warning("Fail to decode '%s'", row)
			
			print row
			yield data


	def issue_dates(self, file_import):
		#c = file_import.content[:64]
		m = re.search(r'([A-Z][a-z]+)_(\d{4})_Sale', file_import.name)
		if m:
			month_name = m.group(1)
			year = int(m.group(2))
			month = 0
			for i in xrange(1, 12):
				if month_name == calendar.month_name[i]:
					month = i
					break
			print 'MONTH', year, month_name, month
			if month > 0:
				(first_weekday, days_in_month) = calendar.monthrange(year, month)
				begin_date = date(year, month, 1)
				end_date = date(year, month, days_in_month)
				return (begin_date, end_date)
		logger.warning("Failed to convert effective_dates for %s", file_import.name)
		return None


	#def update_fields(self, fields):
		#"""Update Fields"""
		#pass
