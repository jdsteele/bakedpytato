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
from plugin.base_supplier_catalog_plugin import BaseSupplierCatalogPlugin

logger = logging.getLogger(__name__)

class SupplierCatalogExactrailPlugin(BaseSupplierCatalogPlugin):
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

		m = re.search('(\d{4})(\d{2})(\d{2}).csv$', file_import.name)
		if m:
			return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))

		logger.warning("Failed to convert issue_date for %s", file_import.name)
		return file_import.effective
