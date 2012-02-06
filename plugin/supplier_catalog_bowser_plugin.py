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
#import uuid
#from decimal import *

#Extended Library
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
	
	column_names11 = ['Manufacturer', 'Item', 'Description1', 'Price1', 'Category1', 'Category2', 'Category3', 'Stock', 'Description2', 'Retail', 'Discount']
	column_names10 = ['Manufacturer', 'Item', 'Description1', 'Price1', 'Category1', 'Category2', 'Category3', 'Stock', 'Retail', 'Discount']

	def match_file_import(self, file_import):
		if re.search('lock', file_import.name):
			return False
		if not re.search('DealerOutsideWebExport', file_import.name):
			return False
		if re.search('Bowser', file_import.content[:1000]):
			return True
		return False

	def get_items(self, supplier_catalog):
		content = supplier_catalog.file_import.content
		lines = re.split("\n", content)
		reader = csv.reader(lines, delimiter="\t")
		for row in reader:
			l = len(row)
			if l == 10:
				column_names = self.column_names10
			elif l == 11:
				column_names = self.column_names11
			else:
				logger.warning("Row has incorrect length: expected 10-11, got %i '%s'", l, row)
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
