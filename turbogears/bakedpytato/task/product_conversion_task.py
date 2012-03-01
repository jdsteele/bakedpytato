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
### Pragma
from __future__ import unicode_literals

### Standard Library
import uuid

### Extended Library
from sqlalchemy.orm.exc import NoResultFound

### Application Library
from bakedpytato.model import metadata, DBSession
from bakedpytato.model import ProductConversionModel
from bakedpytato.model import SupplierCatalogItemModel
from bakedpytato.task.base_task import BaseTask


class ProductConversionTask(BaseTask):
	
	def __init__(self):
		"""Init"""
		self.session = Session(autocommit=True)
	
	
	def load_all_supplier_catalog_items(self):
		"""Load All SupplierCatalogItems"""
		
		query = self.session.query(SupplierCatalogItemModel)

		count = query.count()
		i = 0;

		ts = self.term_stat('Load SupplierCatalogItem', count)

		for supplier_catalog_item in query.yield_per(1000):
			self.session.begin()
			self.load_one_supplier_catalog_item(supplier_catalog_item)
			self.session.commit()
			ts['done'] += 1


	def load_one_supplier_catalog_item(self, supplier_catalog_item):
		pass
