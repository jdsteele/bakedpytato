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
import csv
import logging 
import re
from datetime import datetime
from decimal import *

#Extended Library

#Application Library

#This Package
from plugin.base_supplier_catalog_plugin import BaseSupplierCatalogPlugin

logger = logging.getLogger(__name__)

class SupplierCatalogEmeryPlugin(BaseSupplierCatalogPlugin):

	def match_file_import(self, file_import):
		if re.search('lock', file_import.name):
			return False
		if re.search('emery', file_import.name):
			return True
		return False
		
	def get_items(self, supplier_catalog):
		content = supplier_catalog.file_import.content
		lines = re.split("\n", content)
		reader = csv.reader(lines, delimiter="\t")
		
		column_names = reader.next()
		expected_row_len = len(column_names)
		
		for row in reader:
			if len(row) != expected_row_len:
				logger.warning("Row has incorrect length: expected %i, got %i '%s'", expected_row_len, len(row), row)
				continue

			item = dict()
			i = 0
			for column_name in column_names:
				field = row[i]
				field = field.decode('latin_1').encode('utf-8')
				item[column_name] = field
				i += 1
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

		if fields['VPARTNO'] is not None:
			m = re.match(r'^(...)(.+)$', fields['VPARTNO'])
			data['manufacturer_identifier'] = m.group(1)
			data['product_identifier'] = m.group(2)

		if fields['DESCRIP'] is not None:
			data['name'] = fields['DESCRIP']
			#for removable in self.removables:
			#	data['name'] = re.sub(removable, ' ', data['name'])

		if fields['SCALE'] is not None:
			data['scale_identifier'] = fields['SCALE']

		if fields['CATEGORY'] is not None:
			data['category_identifier'] = fields['CATEGORY']

		if fields['INSTOCK'] is not None:
			if fields['INSTOCK'] in ['YES', 'NO']:
				data['stock'] = (fields['INSTOCK'] == 'YES')
			else:
				logger.error("Field INSTOCK has unexpected value %s", fields['INSTOCK'])

		if fields['ENDOFLIFE'] is not None:
			if fields['ENDOFLIFE'] in ['DISC']:
				data['phased_out'] = (fields['ENDOFLIFE'] == 'DISC')
			else:
				logger.error("Field ENDOFLIFE has unexpected value %s", fields['ENDOFLIFE'])

		if fields['PRICE'] is not None:
			data['retail'] = Decimal(fields['PRICE'])
			if data['retail'] < Decimal(0):
				data['retail'] = Decimal(0)
		else:
			data['retail'] = Decimal(0)

		
		if fields['COST'] is not None:
			cost = Decimal(fields['COST'])

			if cost < Decimal(0):
				cost = Decimal(0)

			if 'special' in data and data['special'] == True:
				data['special_cost'] = cost
			else:
				data['cost'] = cost
		else:
			cost = Decimal(0)

		return data
