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
#import hashlib
#import json
import logging 
#import re

#Extended Library
from sqlalchemy.orm.exc import NoResultFound

#Application Library
#import model
from model import SupplierCatalogItemFieldModel
#from model import SupplierCatalogItemFieldModel
#from model import SupplierCatalogModel

#This Package
from task.base_supplier_catalog_task import BaseSupplierCatalogTask

logger = logging.getLogger(__name__)

class SupplierCatalogItemFieldTask(BaseSupplierCatalogTask):
	
	def update_all(self):
		"""Update All"""
		logger.debug("Begin update_all()")
		self.plugins = self.load_plugins()
		query = self.session.query(SupplierCatalogItemFieldModel)
		self.ts = self.term_stat('SupplierCatalogItemField Update All', query.count())
		for supplier_catalog_item_field in query.yield_per(100):
			self.update_one(supplier_catalog_item_field)
			self.ts['done'] += 1
		self.ts.finish()
		logger.debug("End load_all()")
			
	def update_one(self, supplier_catalog_item_field):
		if not supplier_catalog_item_field.supplier_catalog_filter_id in self.plugins:
			logger.warning("Plugin %s Not Found", supplier_catalog_item_field.supplier_catalog_filter_id)
			return None
		plug = self.plugins[supplier_catalog_item_field.supplier_catalog_filter_id]
