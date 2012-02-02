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
import logging 
import re
from datetime import datetime

#Extended Library

#Application Library

#This Package
from plugin.base_plugin import BasePlugin

logger = logging.getLogger(__name__)

class SupplierCatalogWalthersPlugin(BasePlugin):
	
	supplier_catalog_filter = None

	def __init__(self, supplier_catalog_filter):
		BasePlugin.__init__(self)
		self.supplier_catalog_filter = supplier_catalog_filter

	def match_file_import(self, file_import):
		if re.search('lock', file_import.name):
			return False
		if re.search(r'walthers/CatalogUpdate-\d{8}', file_import.name):
			return True
		return False

	""" *** Getter Functions *** """
	def supplier_id(self):
		return self.supplier_catalog_filter.supplier_id

	def supplier_catalog_filter_id(self):
		return self.supplier_catalog_filter.id
		
	def issue_date(self, file_import):

		m = re.match('(\d{4})(\d{2})(\d{2})', file_import.content[:8])
		if m:
			return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))

		logger.warning("Failed to convert issue_date for %s", file_import.name)
		return file_import.effective
