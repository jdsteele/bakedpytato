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
import chardet
import json
import logging 
import transaction
import uuid
from datetime import datetime
from decimal import Decimal

### Extended Library
from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import ttystatus

### Application Library
from bakedpytato import cfg
from bakedpytato.model import metadata, DBSession
from bakedpytato.model import FileImportModel
from bakedpytato.model import SupplierCatalogFilterModel
from bakedpytato.model import SupplierCatalogItemModel
from bakedpytato.model import SupplierCatalogModel
from bakedpytato.model import SupplierModel
from bakedpytato.task import SettingTask
from bakedpytato.task.base_supplier_catalog_task import BaseSupplierCatalogTask


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
		ts = self.term_stat('SupplierCatalog Load')
		tx = transaction.get()
		
		try:
			plugins = self.load_plugins()
			query = DBSession.query(FileImportModel)
			if modified_since:
				query = query.filter(FileImportModel.modified >= modified_since)
			ts['total'] = query.count()
			for file_import in query.yield_per(1):
				for plug in plugins.itervalues():
					is_match = plug.match_file_import(file_import)
					if is_match:
						self.load_one(plug, file_import)
						break
				DBSession.expunge(file_import)
				ts['done'] += 1
		except Exception:
			logger.exception("Caught Exception: ")
			tx.abort()
		finally:
			ts.finish()
		transaction.commit()
		logger.debug("End load_all()")


	def load_one(self, plug, file_import):
		"""Load One"""
		query = DBSession.query(SupplierCatalogModel)
		query = query.filter(SupplierCatalogModel.file_import_id == file_import.id)
		
		if query.count() == 0:
			supplier_catalog = SupplierCatalogModel()
			DBSession.add(supplier_catalog)
			supplier_catalog.file_import_id = file_import.id
		else:
			supplier_catalog = query.one()
			
		supplier_catalog.supplier_id = plug.supplier_id()
		supplier_catalog.supplier_catalog_filter_id = plug.supplier_catalog_filter_id()
		if not supplier_catalog.lock_issue_date:
			supplier_catalog.issue_date = plug.issue_date(file_import)

	def update(self):
		self.update_all()

	def update_all(self):
		"""Update All"""
		logger.debug("Begin update_all()")
		self.sort()
		#self.update_encoding()
		logger.debug("End update_all()")
		
	def update_encoding(self):
		logger.debug("Begin update_encoding()")
		ts = self.term_stat('SupplierCatalog UpdateEncoding')
		plugins = self.load_plugins()
		tx = transaction.get()
		try:
			query = DBSession.query(SupplierCatalogModel)
			query = query.order_by(desc(SupplierCatalogModel.created))
			ts['total'] = query.count()
			for supplier_catalog in query.yield_per(100):
				if supplier_catalog.supplier_catalog_filter_id is None:
					continue
				#if supplier_catalog.encoding is None:
				if True:
					plug = plugins[supplier_catalog.supplier_catalog_filter_id]
					encoding = plug.get_encoding(supplier_catalog)
					if encoding is None:
						encoding = plug.default_encoding
					supplier_catalog.encoding = encoding['encoding']
				DBSession.expunge(supplier_catalog.file_import)
			ts['done'] += 1
		except Exception:
			logger.exception("Caught Exception: ")
			tx.rollback()
		finally:
			ts.finish()
		logger.debug("update_encoding()")


	def sort(self):
		logger.debug("Begin sort()")
		tx = transaction.get()
		try:
			query = DBSession.query(SupplierModel)
			ts = self.term_stat('SupplierCatalog Sort', query.count())
			suppliers = query.all()
			
			for supplier in suppliers:
				#print supplier
				query = DBSession.query(SupplierCatalogModel)
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
		except Exception:
			logger.exception("Caught Exception: ")
			tx.rollback()
		finally:
			ts.finish()
		logger.debug("End sort()")
