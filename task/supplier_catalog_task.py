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
import uuid
from datetime import datetime
from decimal import *

#Extended Library
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import ttystatus

#Application Library
from model import FileImportModel
from model import SupplierModel
from model import SupplierCatalogModel
from model import SupplierCatalogFilterModel
from model import SupplierCatalogItemModel
import cfg

#This Package
from task.base_supplier_catalog_task import BaseSupplierCatalogTask
from task.setting_task import SettingTask

logger = logging.getLogger(__name__)

class SupplierCatalogTask(BaseSupplierCatalogTask):

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
		logger.debug("Begin load_all()")
		try:
			self.session.begin(subtransactions=True)
			plugins = self.load_plugins()
			query = self.session.query(FileImportModel)
			if modified_since:
				query = query.filter(FileImportModel.modified >= modified_since)
			ts = self.term_stat('SupplierCatalog Load All', query.count())
			for file_import in query.yield_per(1):
				#print file_import.name
				for plug in plugins.itervalues():
					is_match = plug.match_file_import(file_import)
					if is_match:
						self.load_one(plug, file_import)
						break
				self.session.expunge(file_import)
				ts['done'] += 1
			self.session.commit()
		except Exception:
			logger.exception("Caught Exception: ")
			if self.session.transaction is not None:
				self.session.rollback()
		finally:
			ts.finish()
		logger.debug("End load_all()")


	def load_one(self, plug, file_import):
		"""Load One"""
		query = self.session.query(SupplierCatalogModel)
		query = query.filter(SupplierCatalogModel.file_import_id == file_import.id)
		
		self.session.begin(subtransactions=True)
		if query.count() == 0:
			supplier_catalog = SupplierCatalogModel()
			self.session.add(supplier_catalog)
			supplier_catalog.file_import_id = file_import.id
		else:
			supplier_catalog = query.one()
			supplier_catalog.supplier_id = plug.supplier_id()
			supplier_catalog.supplier_catalog_filter_id = plug.supplier_catalog_filter_id()
			if not supplier_catalog.lock_issue_date:
				supplier_catalog.issue_date = plug.issue_date(file_import)
		self.session.commit()

	def update(self):
		self.update_all()

	def update_all(self):
		"""Update All"""
		logger.debug("Begin update_all()")
		self.sort()
		logger.debug("End update_all()")
		
	def sort(self):
		logger.debug("Begin sort()")
		try:
			self.session.begin(subtransactions=True)
			query = self.session.query(SupplierModel)
			ts = self.term_stat('SupplierCatalog Sort', query.count())
			suppliers = query.all()
			
			for supplier in suppliers:
				#print supplier
				query = self.session.query(SupplierCatalogModel)
				query = query.filter(SupplierCatalogModel.supplier_id == supplier.id)
				query = query.order_by(SupplierCatalogModel.issue_date)
				
				prev_supplier_catalog = None
				for supplier_catalog in query:
					#print supplier_catalog
					if prev_supplier_catalog is not None:
						prev_supplier_catalog.next_supplier_catalog_id = supplier_catalog.id
						supplier_catalog.prev_supplier_catalog_id = prev_supplier_catalog.id
					supplier_catalog.next_supplier_catalog_id = None
					prev_supplier_catalog = supplier_catalog
					ts['sub_done'] += 1
				ts['done'] += 1
				ts['sub_done'] = 0
			self.session.commit()
		except Exception:
			logger.exception("Caught Exception: ")
			if self.session.transaction is not None:
				self.session.rollback()
		finally:
			ts.finish()
		logger.debug("End sort()")
