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

#Standard Library
import csv
import logging 
import re
import cfg
from datetime import datetime
from decimal import *

#Extended Library

#Application Library

#This Package
from plugin.base_supplier_catalog_plugin import BaseSupplierCatalogPlugin

logger = logging.getLogger(__name__)

class SupplierCatalogEmeryPlugin(BaseSupplierCatalogPlugin):

	default_encoding = 'ISO-8859-1'

	def match_file_import(self, file_import):
		if re.search('lock', file_import.name):
			return False
		if re.search('emery', file_import.name):
			return True
		if re.match(cfg.emery_user + 'xp-20\d{6}.CSV', file_import.name):
			return True
		return False
		
	def get_items(self, supplier_catalog):
		content = supplier_catalog.file_import.content
		lines = re.split(bytes("\n"), content)
		reader = csv.reader(lines, delimiter=bytes("\t"))
		
		column_names = reader.next()
		
		expected_row_len = len(column_names)
		
		for row in reader:
			if row is None or row == []:
				yield None
				continue

			item = dict()
			i = 0
			for column_name in column_names:
				if len(row) > i:
					field = row[i]
					field = field.strip()
					if field == bytes(''):
						field = None
					item[column_name] = field
				i += 1
			item = self.recode(item)
			yield item

	def issue_date(self, file_import):

		m = re.search('(\d{4})(\d{2})(\d{2}).CSV$', file_import.name)
		if m:
			return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))

		logger.warning("Failed to convert issue_date for %s", file_import.name)
		return file_import.effective

	def update_fields(self, fields):
		"""Update Field"""

		#'VPARTNO', 'DESCRIP', 'SCALE', 'CATEGORY', 'PRICE', 'COST', 'INSTOCK', 'ENDOFLIFE', 'ONSALE', 

		if fields is None:
			logger.warning("Fields is empty")
			return None

		data = dict()

		if 'VPARTNO' in fields:
			m = re.match(r'^(...)(.+)$', fields['VPARTNO'])
			data['manufacturer_identifier'] = m.group(1)
			data['product_identifier'] = m.group(2)

		if 'DESCRIP' in fields:
			data['name'] = fields['DESCRIP']
			#for removable in self.removables:
			#	data['name'] = re.sub(removable, ' ', data['name'])

		if 'SCALE' in fields:
			data['scale_identifier'] = fields['SCALE']

		if 'CATEGORY' in fields:
			data['category_identifier'] = fields['CATEGORY']

		if 'INSTOCK' in fields:
			if fields['INSTOCK'] in [None, 'YES', 'NO']:
				data['stock'] = (fields['INSTOCK'] == 'YES')
			else:
				logger.error("Field INSTOCK has unexpected value %s", fields['INSTOCK'])

		if 'ENDOFLIFE' in fields:
			if fields['ENDOFLIFE'] in [None, 'DISC']:
				data['phased_out'] = (fields['ENDOFLIFE'] == 'DISC')
			else:
				logger.error("Field ENDOFLIFE has unexpected value %s", fields['ENDOFLIFE'])

		if 'PRICE' in fields:
			data['retail'] = Decimal(fields['PRICE'])
			if data['retail'] < Decimal(0):
				data['retail'] = Decimal(0)
		else:
			data['retail'] = Decimal(0)

		if 'ONSALE' in fields:
			if fields['ONSALE'] in [None, 'Yes', 'No']:
				data['special'] = (fields['ONSALE'] == 'Yes')
			else:
				logger.error("Field ONSALE has unexpected value %s", fields['ONSALE'])

		
		if 'COST' in fields:
			cost = Decimal(fields['COST'])

			if cost < Decimal(0):
				cost = Decimal(0)

			if 'special' in data and data['special'] == True:
				data['special_cost'] = cost
				data['cost'] = Decimal(0)
			else:
				data['cost'] = cost
				data['special_cost'] = Decimal(0)
		else:
			data['cost'] = Decimal(0)
			data['special_cost'] = Decimal(0)

		data = self.recode(data)

		return data
