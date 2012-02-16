# -*- coding: utf-8 -*-
"""
	BakedPotato — Inventory Management System

	BakedPotato IMS
	Copyright 2010-2012, John David Steele (john.david.steele@gmail.com)

	Licensed under The MIT License
	Redistributions of files must retain the above copyright notice.

	@copyright     Copyright 2010-2012, John David Steele (john.david.steele@gmail.com)
	@license       MIT License (http://www.opensource.org/licenses/mit-license.php)'cmp-
"""
#Standard Library
import csv
import logging 
import re
from datetime import datetime

#Extended Library

#Application Library

#This Package
from plugin.base_supplier_catalog_plugin import BaseSupplierCatalogPlugin, Empty

logger = logging.getLogger(__name__)

class SupplierCatalogExactrailPlugin(BaseSupplierCatalogPlugin):


	prefixes = {
		'EN':['N', 'Freight Rolling Stock'],
		'EE':['HO', 'Freight Rolling Stock'],
		'EP':['HO', 'Freight Rolling Stock'],
		'EPS':['HO', 'Freight Rolling Stock'],
		'EX':['HO', 'Freight Rolling Stock'],
		'ET':['HO', 'Trucks'],
		'EW':['HO', 'Wheels'],
		'EWN':['N', 'Wheels']
	}
	
	categories = [
		'48\' Depressed Center Flat Car',
		'72\' Deck Plate Girder Bridge',
		'Evans 4780 Covered Hopper',
		'Evans 5277 .+ Box Car',
		'Gunderson 2,420 Gondola',
		'Gunderson 5200 Box Car',
		'Gunderson 7466 Wood Chip Gondola',
		'AutoFlood II Coal Hopper',
		'40\' Rib Side Box Car',
		'Beer Car',
		'PS-2CD .+ Covered Hopper',
		'PS 50\' Waffle Box Car',
		'P-S 7315 Waffle Box Car',
		'Thrall 3564 Gondola',
		'FMC 5277 Combo Door Box Car',
		'Trinity 50\' Hy-Cube Box Car',
		'Trinity 5161 Cylindrical Hopper',
		'PC&F 6033 cu. ft. Hy-Cube Box',
		'Vert-A-Pac Automobile Car',
	]

	
	
	def match_file_import(self, file_import):
		if re.search('lock', file_import.name):
			return False
		if re.search('exactrail', file_import.name):
			return True
		return False
		
	def get_items(self, supplier_catalog):
		content = supplier_catalog.file_import.content
		lines = re.split("\n", content)
		reader = csv.reader(lines, delimiter=",")
		
		column_names = reader.next()
		column_names = column_names.capitalize()
		
		expected_row_len = len(column_names)
		
		for row in reader:
			
			if row is None:
				yield Empty
				continue
			
			if len(row) != expected_row_len:
				logger.warning("Row has incorrect length: expected %i, got %i '%s'", expected_row_len, len(row), row)
				yield Empty
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

		m = re.search('(\d{4})(\d{2})(\d{2}).csv$', file_import.name)
		if m:
			return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))

		logger.warning("Failed to convert issue_date for %s", file_import.name)
		return file_import.effective

	def update_fields(self, fields):
		"""Update Field"""

		if fields is None:
			logger.warning("Fields is empty")
			return Empty

		data = dict()

		data['manufacturer_identifier'] = '253'

		if fields['UPC/SKU'] is not None:
			data['product_identifier'] = fields['UPC/SKU']
		if fields['ROAD NAME'] is not None:
				data['name'] = data['name'] + ' ' + fields['ROAD NAME']
		if fields['ROAD #S\''] is not None:
				data['name'] = data['name'] + ' ' + fields['ROAD #S\'']

		if fields['DESCRIPTION'] is not None:
			data['name'] = fields['DESCRIPTION']
			
		if fields['UPC/SKU'] is not None:
			(prefix, body) = split(r'-', fields['UPC/SKU'], 2)
			default_category = None
			if prefix in self.prefixes:
				(scale, default_category) = self.prefixes[prefix]
				data['scale_identifier'] = scale
			else:
				logger.warning("No Prefix Found for %s", fields['UPC/SKU'])
				data['scale_identifier'] = Empty
			
			for category in self.categories:
				if re.match(category, fields['DESCRIPTION']):
					fields['category_identifier'] = category
			
			if not defined(fields['category_identifier']):
				data['category_identifier'] = default_category
				logger.warning("No Category Found for %s", fields['DESCRIPTION'])
				data['category_identifier'] = Empty

		if fields['STOCK'] is not None:
			if fields['STOCK'] in ['In Stock', '< 25 Call', '< 25 call', 'Pre-Order']:
				data['stock'] = (fields['STOCK'] in ['In Stock', '** NEW **'])
				data['advanced'] = (fields['STOCK'] == 'Pre-Order')
			else:
				logger.error("Field INSTOCK has unexpected value %s", fields['STOCK'])
				data['stock'] = Empty
				data['advanced'] = Empty

		if fields['MSRP'] is not None:
			data['retail'] = Decimal(fields['MSRP'].strip('$'))
			if data['retail'] < Decimal(0):
				data['retail'] = Decimal(0)
		else:
			data['retail'] = Empty

		
		if fields['COST'] is not None:
			cost = Decimal(fields['DEALER'].strip('$'))

			if cost < Decimal(0):
				cost = Empty

			if 'special' in data and data['special'] == True:
				data['special_cost'] = cost
				data['cost'] = Empty
			else:
				data['cost'] = cost
				data['special_cost'] = Empty
		else:
			cost = Empty

		return data
