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
from decimal import Decimal
from datetime import datetime

#Extended Library

#Application Library

#This Package
from plugin.base_supplier_catalog_plugin import BaseSupplierCatalogPlugin

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
		r'40\' Rib Side Box Car',
		r'48\' Depressed Center Flat Car',
		r'72\' Deck Plate Girder Bridge',
		r'AutoFlood II Coal Hopper',
		r'Beer Car',
		r'B&O M-53 Wagontop Box Car',
		r'Evans 4780 Covered Hopper',
		r'Evans 5277 .+ Box Car',
		r'FMC 5277 Combo Door Box Car',
		r'FMC 4000 Gondola',
		r'Gunderson 2,420 Gondola',
		r'Gunderson 5200 Box Car',
		r'Gunderson 7466 Wood Chip Gondola',
		r'PC&F 6033 cu. ft. Hy-Cube Box Car',
		r'PS-2CD .+ Covered Hopper',
		r'PS 50\' Waffle Box Car',
		r'P-S 7315 Waffle Box Car',
		r'Thrall 3564 Gondola',
		r'Trinity 50\' Hy-Cube Box Car',
		r'Trinity 5161 Cylindrical Hopper',
		r'Vert-A-Pac Automobile Car',
	]

	
	
	def match_file_import(self, file_import):
		if re.search('lock', file_import.name):
			return False
		if re.search('exactrail', file_import.name):
			return True
		if re.search('exact_rail', file_import.name):
			return True
		if re.match('20\d{6}\.csv', file_import.name):
			return True
		return False
		
	def get_items(self, supplier_catalog):
		content = supplier_catalog.file_import.content
		lines = re.split("\n", content)
		reader = csv.reader(lines, delimiter=",")
		
		column_names = reader.next()
		for i in xrange(len(column_names)):
			column_names[i] = column_names[i].upper()
		
		expected_row_len = len(column_names)
		
		for row in reader:
			
			if row is None:
				yield None
				continue
			
			if len(row) != expected_row_len:
				logger.warning("Row has incorrect length: expected %i, got %i '%s'", expected_row_len, len(row), row)
				yield None
				continue

			item = dict()
			i = 0
			for column_name in column_names:
				#print "C", column_name
				field = row[i]
				field = field.decode('latin_1').encode('utf-8')
				item[column_name] = field
				i += 1
			yield item

	def issue_date(self, file_import):

		m = re.search('(\d{4})(\d{2})(\d{2}).csv$', file_import.name)
		if m:
			try:
				d = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
				return d
			except Exception:
				logger.exception("Caught Exception '%s': ", file_import.name)

		logger.warning("Failed to convert issue_date for %s", file_import.name)
		return file_import.effective

	def update_fields(self, fields):
		"""Update Field"""

		if fields is None:
			logger.warning("Fields is empty")
			return None

		data = dict()

		data['manufacturer_identifier'] = '253'

		if 'DESCRIPTION' in fields:
			data['name'] = fields['DESCRIPTION']

		if 'UPC/SKU' in fields:
			data['product_identifier'] = fields['UPC/SKU']
		if 'ROAD NAME' in fields and fields['ROAD NAME'] != 'None':
				data['name'] = data['name'] + ' ' + fields['ROAD NAME']
		if 'ROAD #S\'' in fields and fields['ROAD #S\''] != 'None':
				data['name'] = data['name'] + ' ' + fields['ROAD #S\'']

		data['category_identifier'] = None
		if 'UPC/SKU' in fields:
			(prefix, body) = fields['UPC/SKU'].split('-', 1)
			default_category = None
			if prefix in self.prefixes:
				(scale, default_category) = self.prefixes[prefix]
				data['scale_identifier'] = scale
			else:
				logger.warning("No Prefix Found for %s", fields['UPC/SKU'])
				data['scale_identifier'] = None
			
			for category in self.categories:
				m = re.search(category, fields['DESCRIPTION'])
				if m:
					data['category_identifier'] = m.group(0)

			if data['category_identifier'] is None:
				data['category_identifier'] = default_category
				logger.warning("No Category Found for %s", fields['DESCRIPTION'])

		if 'STOCK' in fields:
			if fields['STOCK'] in ['OOS', 'In Stock', '< 25 Call', '< 25 call', 'Pre-Order']:
				data['stock'] = (fields['STOCK'] in ['In Stock', '** NEW **'])
				data['advanced'] = (fields['STOCK'] == 'Pre-Order')
			else:
				logger.error("Field INSTOCK has unexpected value %s", fields['STOCK'])
				data['stock'] = None
				data['advanced'] = None

		if 'MSRP' in fields:
			data['retail'] = Decimal(fields['MSRP'].strip('$'))
			if data['retail'] < Decimal(0):
				data['retail'] = Decimal(0)
		else:
			data['retail'] = Decimal(0)

		
		if 'DEALER' in fields:
			cost = Decimal(fields['DEALER'].strip('$'))

			if cost < Decimal(0):
				cost = Decimal(0)

			if 'special' in data and data['special'] == True:
				data['special_cost'] = cost
				data['cost'] = Decimal(0)
			else:
				data['cost'] = cost
				data['special_cost'] = Decimal(0)
		else:
			cost = Decimal(0)

		return data
