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

class SupplierSpecialWalthersPlugin(BaseSupplierSpecialPlugin):
	
	default_encoding = 'ISO-8859-1'
	
	patterns = [
		r'(\d.{13}) (.{30})(.{5})([\d. ]{8})([\d. ]{7})(\d{2}%)',
		r'(\d.{13}) (.{26})(.{9})([\d. ]{7})([\d. ]{8})(\d{2}%)',
		r'(\d.{12}) (.{26})(.{8})([\d. ]{9})([\d. ]{7})(\d{2}%)', #from 20100301

	]

	#'920-47951     E7A-A Set DC MILW #19A/B  H        329.98 164.99  50%'


	def match_file_import(self, file_import):
		if re.search('lock', file_import.name):
			return False
		if not re.search(r'walthers/{1,2}Specials[ -]\d{8}', file_import.name):
			return False
		magic = file_import.magic()
		if magic['mime'] != 'text/plain':
			return False
		if magic['magic'] != 'ASCII text':
			return False
		return True

	def get_items(self, supplier_special):
		content = supplier_special.file_import.content
		lines = re.split(r"\n", content)
		for row in lines:
			
			if row.startswith(bytes('Prices valid')):
				continue
			if row.startswith(bytes('Pricing valid')):
				continue
			if row.startswith(bytes('Prices are valid')):
				continue

			if row.startswith(bytes('MANU-ITEM')):
				continue
			if row.endswith(bytes('Hotlist')):
				continue
			
			if re.match(r'^\d+/\d+/\d+$', row):
				continue
			
			if row == '':
				yield None
				continue
			data = dict()

			m = re.match(r'^(\d+)\-(.{1,10})\s\s+(.*)\s+([\d.]+)\s+([\d.]+)\s+([\d]+%)', row)
			if m:
				pass
				data['MANU'] = m.group(1).strip()
				data['ITEM'] = m.group(2).strip()
				remainder = m.group(3).strip()
				data['RET'] =	m.group(4).strip()
				data['DLR'] = m.group(5).strip()
				data['DISC'] = m.group(6).strip()
			else:
				logger.warning("Fail to decode '%s' from '%s'", row, supplier_special.file_import.name)
			
			data = self.recode(data)
			#print data
			yield data


	def issue_dates(self, file_import):
		c = file_import.content[:64]
		start_date = None
		end_date = None
		### Beware, Walthers apparently has never heard of Y2K...
		
		### ie: Prices valid from 12/9 thru 12/31/11
		m = re.search('from (\d{1,2})[-/](\d{1,2}) thru (\d{1,2})[-/](\d{1,2})[-/](\d{2,4})', c)
		if m:
			start_month = int(m.group(1))
			start_day = int(m.group(2))
			end_month = int(m.group(3))
			end_day = int(m.group(4))
			start_year = end_year = int(m.group(5)) + 2000
			
			start_date = date(start_year, start_month, start_day)
			end_date = date(end_year, end_month, end_day)
			
		### ie: Pricing valid from 11/25/11 thru 12/13/11
		m = re.search(r'from (\d{1,2})[-/](\d{1,2})[-/](\d{2,4}) thru (\d{1,2})[-/](\d{1,2})[-/](\d{2,4})', c)
		if m:
			start_month = int(m.group(1))
			start_day = int(m.group(2))
			start_year = int(m.group(3))
			end_month = int(m.group(4))
			end_day = int(m.group(5))
			end_year = int(m.group(6)) + 2000
			start_date = date(start_year, start_month, start_day)
			end_date = date(end_year, end_month, end_day)
			
			
		### ie: Prices valid thru 7/23/11
		m = re.search(r'thru (\d{1,2})[-/](\d{1,2})[-/](\d{2,4})', c)
		if m:
			end_month = int(m.group(1))
			end_day = int(m.group(2))
			end_year = int(m.group(3)) + 2000
			end_date = date(end_year, end_month, end_day)
			start_date = end_date - timedelta(days=14)

		### ie: Prices are valid thru 5/10
		m = re.search(r'thru (\d{1,2})[-/](\d{2,4})', c)
		if m:
			end_year = file_import.effective.year
			end_month = int(m.group(1))
			end_day = int(m.group(2))
			end_date = date(end_year, end_month, end_day)
			start_date = end_date - timedelta(days=14)
		if start_date is not None and end_date is not None:
			return(start_date, end_date)
		logger.warning("Failed to convert effective_dates for %s", file_import.name)
		return None


	#def update_fields(self, fields):
		#"""Update Fields"""
		#pass
