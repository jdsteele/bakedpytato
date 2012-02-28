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
#Standard Library
import logging 
import re
import struct
import tempfile
from datetime import datetime
from decimal import *

#Extended Library

#Application Library

#This Package
from plugin.base_supplier_special_plugin import BaseSupplierSpecialPlugin

logger = logging.getLogger(__name__)


class SupplierSpecialWalthersPlugin(BaseSupplierSpecialPlugin):
	
	patterns = [
		r'(\d.{13}) (.{30})(.{5})([\d. ]{8})([\d. ]{7})(\d{2}%)',
		r'(\d.{12}) (.{26})(.{8})([\d. ]{9})([\d. ]{7})(\d{2}%)' #from 20100301
	]

	def match_file_import(self, file_import):
		if re.search('lock', file_import.name):
			return False
		if re.search(r'walthers/{1,2}Specials[ -]\d{8}', file_import.name):
			return True
		return False

	def get_items(self, supplier_special):
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

	def issue_date(self, file_import):

		m = re.match('(\d{4})(\d{2})(\d{2})', file_import.content[:8])
		if m:
			return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))

		logger.warning("Failed to convert issue_date for %s", file_import.name)
		return file_import.effective


	#def update_fields(self, fields):
		#"""Update Fields"""
		#pass
