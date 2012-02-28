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
import logging 
import uuid
from datetime import datetime
from decimal import Decimal

### Extended Library
import ttystatus
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

### Application Library
from bakedpytato import cfg
from bakedpytato.model import metadata, DBSession
from bakedpytato.model import FileImportModel
from bakedpytato.model import SupplierSpecialFilterModel
from bakedpytato.model import SupplierSpecialModel
from bakedpytato.task import SettingTask
from bakedpytato.task.base_supplier_special_task import BaseSupplierSpecialTask


logger = logging.getLogger(__name__)

class SupplierSpecialTask(BaseSupplierSpecialTask):

	def load(self):
		"""Update"""
		logger.debug("Begin load()")
		self.load_modified()
		logger.debug("End load()")
		

	def load_modified(self):
		logger.debug("Begin load_modified()")
		
		start_time = datetime.now()
		
		modified_since = SettingTask().get(__name__, 'load.last_modified', datetime(1970,1,1))
		logger.info("Load ModifiedSince %s", modified_since)
		self.load_all(modified_since)
		SettingTask().set(__name__, 'load.last_modified', start_time)
		logger.debug("End load_modified()")

	def load_all(self, modified_since=None):
		"""Load All"""
		pass
		logger.debug("Begin load_all()")
		plugins = self.load_plugins()
		query = self.session.query(FileImportModel)
		if modified_since:
			query = query.filter(FileImportModel.modified >= modified_since)
		ts = self.term_stat('SupplierSpecial Load', query.count())
		for file_import in query.yield_per(1):
			#print file_import.name
			for plug in plugins.itervalues():
				is_match = plug.match_file_import(file_import)
				if is_match:
					self.load_one(plug, file_import)
					break
			self.session.expunge(file_import)
			ts['done'] += 1
		ts.finish()
		logger.debug("End load_all()")


	def load_one(self, plug, file_import):
		"""Load One"""
		pass
		#query = self.session.query(SupplierCatalogModel)
		#query = query.filter(SupplierCatalogModel.file_import_id == file_import.id)
		
		#self.session.begin()
		#if query.count() == 0:
			#supplier_catalog = SupplierCatalogModel()
			#self.session.add(supplier_catalog)
			#supplier_catalog.file_import_id = file_import.id
		#else:
			#supplier_catalog = query.one()
			#supplier_catalog.supplier_id = plug.supplier_id()
			#supplier_catalog.supplier_catalog_filter_id = plug.supplier_catalog_filter_id()
			#if not supplier_catalog.lock_issue_date:
				#supplier_catalog.issue_date = plug.issue_date(file_import)
		#self.session.commit()

	def update_all(self):
		"""Update All"""
		pass
		logger.debug("Begin update_all()")
		self.sort()
		logger.debug("End update_all()")
		
	def sort(self):
		pass
		#logger.debug("Begin sort()")
		#query = self.session.query(SupplierModel)
		#suppliers = query.all()
		
		#for supplier in suppliers:
			##print supplier
			#query = self.session.query(SupplierCatalogModel)
			#query = query.filter(SupplierCatalogModel.supplier_id == supplier.id)
			#query = query.order_by(SupplierCatalogModel.issue_date)
			
			#prev_supplier_catalog = None
			
			#for supplier_catalog in query:
				##print supplier_catalog
				#if prev_supplier_catalog is not None:
					#prev_supplier_catalog.next_supplier_catalog_id = supplier_catalog.id
					#supplier_catalog.prev_supplier_catalog_id = prev_supplier_catalog.id
				#prev_supplier_catalog = supplier_catalog
			#supplier_catalog.next_supplier_catalog_id = None
		#logger.debug("End sort()")
