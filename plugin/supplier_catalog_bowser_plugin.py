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
from datetime import date, datetime, MINYEAR, MAXYEAR
#import uuid
from decimal import *

#Extended Library
import chardet
#from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
#import ttystatus

#Application Library
#from models import Supplier
#from models import SupplierCatalog
#from models import SupplierCatalogItem
#import cfg


#This Package
from plugin.base_supplier_catalog_plugin import BaseSupplierCatalogPlugin

logger = logging.getLogger(__name__)

class SupplierCatalogBowserPlugin(BaseSupplierCatalogPlugin):
	
	default_encoding = 'ISO-8859-1'
	
	column_names11 = ['Manufacturer', 'Item', 'Description1', 'Price1', 'Category1', 'Category2', 'Category3', 'Stock', 'Description2', 'Retail', 'Discount']
	column_names10 = ['Manufacturer', 'Item', 'Description1', 'Price1', 'Category1', 'Category2', 'Category3', 'Stock', 'Retail', 'Discount']
	
	removables = [
		'Arbour',
		'Atlas',
		'Bowser', 
		'Englishs', 
		"English's",
		'English',
		'Cal Scale',
		'Cary',
		'Selley',
		'Stewart',
		'Walthers'
	]


	def match_file_import(self, file_import):
		if re.search('lock', file_import.name):
			return False
		if not re.search('DealerOutsideWebExport', file_import.name):
			return False
		if re.search('Bowser', file_import.content[:1000]):
			return True
		return False

	def get_encoding(self, supplier_catalog):
		"""Subclass Me"""
		encoding = chardet.detect(supplier_catalog.file_import.content)
		print encoding
		return encoding

	def get_items(self, supplier_catalog):
		content = supplier_catalog.file_import.content
		lines = re.split(bytes("\n"), content)
		reader = csv.reader(lines, delimiter=bytes("\t"))
		for row in reader:
			l = len(row)
			if l == 10:
				column_names = self.column_names10
			elif l == 11:
				column_names = self.column_names11
			else:
				logger.warning("Row has incorrect length: expected 10-11, got %i '%s'", l, row)
				yield None
				continue
				
			item = dict()
			i = 0
			for column_name in column_names:
				field = row[i]
				item[column_name] = field
				i += 1
			item = self.recode(item)
			yield item
		
	def issue_date(self, file_import):

		#5-09-2011 DealerOutsideWebExport
		#7-5-2011 Bowser DealerOutsideWebExport.txt
		m = re.search('(\d{1,2})-(\d{1,2})-(\d{4}) (Bowser ){0,1}DealerOutsideWebExport', file_import.name)
		if m:
			return datetime(int(m.group(3)), int(m.group(1)), int(m.group(2)))

		#11302011 DealerOutsideWebExport.txt
		m = re.search('(\d{2})(\d{2})(\d{4}) DealerOutsideWebExport', file_import.name)
		if m:
			return datetime(int(m.group(3)), int(m.group(1)), int(m.group(2)))

		logger.warning("Failed to convert issue_date for %s", file_import.name)
		return file_import.effective

	def update_fields(self, fields):
		"""Update Field"""

		if fields is None:
			logger.warning("Fields is empty")
			return None

		data = dict()

		if 'Manufacturer' in fields and fields['Manufacturer'] is not None:
			data['manufacturer_identifier'] = fields['Manufacturer']
			
		if 'Item' in fields and fields['Item'] is not None:
			data['product_identifier'] = fields['Item']
			
		if 'Description1' in fields and fields['Description1'] is not None:
			data['name'] = fields['Description1']
			for removable in self.removables:
				data['name'] = re.sub(removable, ' ', data['name'])
			data['name'] = data['name'].lstrip()

		if 'Category1' in fields and fields['Category1'] is not None:
			data['category_identifier'] = fields['Category1']
		elif 'Category2' in fields and fields['Category2'] is not None:
			data['category_identifier'] = fields['Category2']
		elif 'Category3' in fields and fields['Category3'] is not None:
			data['category_identifier'] = fields['Category3']


		if 'Stock' in fields and fields['Stock'] is not None:
			data['stock'] = (int(fields['Stock']) > 0)
			data['advanced'] = (int(fields['Stock']) == -10000)
		
			if data['advanced'] == True:
				m = re.match(r'(\d{1,2})\/(\d{1,2})\/(\d{4})', fields['Description2'])
				if m:
					
					month = int(m.group(1))
					day = int(m.group(2))
					year = int(m.group(3))
					
					if year > 2100:
						data['availability_indefinite'] = True
						data['available'] = date(MAXYEAR, 1, 1)
					else:
						data['available'] = date(year, month, day)
						data['availability_indefinite'] = False
				else:
					data['availability_indefinite'] = True
					data['available'] = date(MAXYEAR, 1, 1)
			else:
				data['availability_indefinite'] = None
				data['available'] = None


		if 'Retail' in fields and fields['Retail'] is not None:
			m = re.match(r'\$(.*)', fields['Retail'])
			if m:
				data['retail'] = m.group(1)
				data['retail'] = re.sub(r'\,', '', data['retail'])
				data['retail'] = data['retail'].strip()
				data['retail'] = Decimal(data['retail'])
			else:
				data['retail'] = Decimal(0)

			if data['retail'] > Decimal(9000):
				##Bowser uses '9999.00' and '9999.99' to indicate 'TBA'
				data['retail'] = Decimal(0)
				data['to_be_announced'] = True

			if data['retail'] < Decimal(0):
				data['retail'] = Decimal(0)
		
			#data['cost'] = fields['Price1']

			if 'Discount' in fields and fields['Discount'] is not None:
				discount = Decimal(fields['Discount'])
				ratio = (Decimal(100) - discount) / Decimal(100)
				data['cost'] = data['retail'] * ratio

			data['phased_out'] = False
			data['special_cost'] = Decimal(0)

		return data
