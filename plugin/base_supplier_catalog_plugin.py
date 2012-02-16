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
from datetime import datetime

#Extended Library

#Application Library

#This Package
from plugin.base_plugin import BasePlugin, Opaque

logger = logging.getLogger(__name__)

class BaseSupplierCatalogPlugin(BasePlugin):
	supplier_catalog_filter = None

	def __init__(self, supplier_catalog_filter):
		BasePlugin.__init__(self)
		self.supplier_catalog_filter = supplier_catalog_filter

	def match_file_import(self, file_import):
		"""Subclass Me"""
		pass
		
	def get_items(self, supplier_catalog):
		"""SubClass Me"""
		return []

	def update_fields(self, supplier_catalog_item_field):
		"""Subclass Me"""
		return

	def supplier_id(self):
		return self.supplier_catalog_filter.supplier_id

	def ghost_stock(self):
		return self.supplier_catalog_filter.ghost_stock

	def ghost_phased_out(self):
		return self.supplier_catalog_filter.ghost_phased_out

	def ghost_advanced(self):
		return self.supplier_catalog_filter.ghost_advanced
		
	def ghost(self):
		return (
			self.supplier_catalog_filter.ghost_stock |
			self.supplier_catalog_filter.ghost_phased_out |
			self.supplier_catalog_filter.ghost_advanced
		)

	def opaque(self):
		return self.supplier_catalog_filter.opaque


	def supplier_catalog_filter_id(self):
		return self.supplier_catalog_filter.id

	def version_model(self):
		return self.supplier_catalog_filter.version_model
		
	def issue_date(self, file_import):
		"""Subclass Me"""
		return file_import.effective

		
