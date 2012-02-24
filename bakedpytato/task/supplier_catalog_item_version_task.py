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
import hashlib
import logging 
import re
import random
from datetime import datetime

#Extended Library
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc
from pybloom import ScalableBloomFilter

#Application Library
import model
from model import SupplierCatalogItemVersionModel
from model import SupplierCatalogItemFieldModel
from model import SupplierCatalogModel

#This Package
from task.base_supplier_catalog_task import BaseSupplierCatalogTask

logger = logging.getLogger(__name__)

#TODO: delete SupplierCatalogItemVersions for empty rows, 
#and rows past last row found in FileImport
#
#vacuum SupplierCatalogItems for non-existant Supplier Catalogs
#
#load modified SupplierCatalogs

class SupplierCatalogItemVersionTask(BaseSupplierCatalogTask):
	
	def load(self):
		"""Load"""
		logger.debug("Begin load()")
		self.load_all(limit=10)
		## TODO: re-load a randomly picked catalog here?
		logger.debug("End load()")
	
	def load_all(self, limit=None, item_versions_loaded=None, supplier_id=None):
		"""Load All"""
		logger.debug("Begin load_all(limit=%s, item_versions_loaded=%s)", limit, item_versions_loaded)
		self.session.begin(subtransactions=True)
		self.ts = self.term_stat('SupplierCatalogItemVersion Load')

		try:
			self.plugins = self.load_plugins()
			query = self.session.query(SupplierCatalogModel)
			alt_query = query.filter(SupplierCatalogModel.supplier_catalog_item_versions_loaded == None)
			
			if alt_query.count() > 0:
				query = alt_query.order_by(desc(SupplierCatalogModel.issue_date))
			else:
				query = query.order_by(SupplierCatalogModel.supplier_catalog_item_versions_loaded)
			del alt_query

			if supplier_id is not None:
				query = query.filter(SupplierCatalogModel.supplier_id == supplier_id)
			else:
				query = query.filter(SupplierCatalogModel.supplier_id != None)

			if limit is not None:
				query = query.limit(limit)

			self.ts['total'] = query.count()
			for supplier_catalog in query.yield_per(10):
				self.load_one(supplier_catalog)
				supplier_catalog.supplier_catalog_item_versions_loaded = datetime.now()
				if self.ts['done'] % 1000 == 0 :
					self.session.flush()
				self.ts['done'] += 1
			self.session.commit()
		except Exception:
			logger.exception('Caught Exception: ')
			if self.session.transaction is not None:
				self.session.rollback()
		finally:
			self.ts.finish()
		logger.debug("End load_all()")
		
	def load_one(self, supplier_catalog):
		self.session.begin(subtransactions=True)
		self.load_from_supplier_catalog(supplier_catalog)
		self.session.commit()
			
	def load_from_supplier_catalog(self, supplier_catalog):
		if not supplier_catalog.supplier_catalog_filter_id in self.plugins:
			logger.warning("Plugin %s Not Found For SupplierCatalog %s", supplier_catalog.supplier_catalog_filter_id, supplier_catalog.id)
			return None
		#self.session.begin(subtransactions=True)
		plug = self.plugins[supplier_catalog.supplier_catalog_filter_id]
		self.ts['sub_done'] = 0
		row_number = 0

		for row in plug.get_items(supplier_catalog):
			self.ts['sub_done'] += 1
			row_number += 1
			supplier_catalog_item_field = self.load_supplier_catalog_item_field(supplier_catalog, row)
			self.load_supplier_catalog_item_version(supplier_catalog, supplier_catalog_item_field, row_number)
		#self.session.commit()

	def load_supplier_catalog_item_field(self, supplier_catalog, row):
		self.session.begin(subtransactions=True)
		if row is not None:
			j = SupplierCatalogItemFieldModel.encode_json(row)
		else:
			j = None

		if j is None:
			supplier_catalog_item_field = None
		else:
			checksum = hashlib.sha1(j).hexdigest()
			plug = self.plugins[supplier_catalog.supplier_catalog_filter_id]
		
			query = self.session.query(SupplierCatalogItemFieldModel)
			query = query.filter(SupplierCatalogItemFieldModel.checksum == checksum)
			try:
				supplier_catalog_item_field = query.one()
			except NoResultFound:
				supplier_catalog_item_field = SupplierCatalogItemFieldModel()
				self.session.add(supplier_catalog_item_field)
		
			supplier_catalog_item_field.fields = j.encode('utf-8')
			supplier_catalog_item_field.checksum = checksum
			supplier_catalog_item_field.supplier_id = supplier_catalog.supplier_id
			supplier_catalog_item_field.supplier_catalog_filter_id = plug.supplier_catalog_filter_id()
		self.session.commit()
		return supplier_catalog_item_field

	def load_supplier_catalog_item_version(self, supplier_catalog, supplier_catalog_item_field, row_number):
		self.session.begin(subtransactions=True)
		plug = self.plugins[supplier_catalog.supplier_catalog_filter_id]
		model_name = plug.version_model()  + 'Model'
		VersionModel = getattr(model, model_name)
		query = self.session.query(VersionModel)
		query = query.filter(VersionModel.supplier_catalog_id == supplier_catalog.id)
		query = query.filter(VersionModel.row_number == row_number)
		
		if supplier_catalog_item_field is None:
			query.delete()
			supplier_catalog_item_version = None
		else:
			try:
				supplier_catalog_item_version = query.one()
			except NoResultFound:
				supplier_catalog_item_version = VersionModel()
				self.session.add(supplier_catalog_item_version)
		
			supplier_catalog_item_version.supplier_catalog_id = supplier_catalog.id
			supplier_catalog_item_version.supplier_catalog_item_field_id = supplier_catalog_item_field.id
			supplier_catalog_item_version.supplier_catalog_filter_id = plug.supplier_catalog_filter_id()
			supplier_catalog_item_version.row_number = row_number
			supplier_catalog_item_version.effective = supplier_catalog.issue_date
		self.session.commit()
		return supplier_catalog_item_version

	def update(self):
		logger.debug("Begin update()")
		self.update_all()
		logger.debug("End update()")

	def update_all(self):
		logger.debug("Begin update_all()")
		self.session.begin(subtransactions=True)
		self.ts = self.term_stat("SupplierCatalogItemVersion update")
		try:
			self.plugins = self.load_plugins()

			query = self.session.query(SupplierCatalogModel)
			self.ts['total'] = query.count()

			for plug in self.plugins.itervalues():
				supplier_catalog_filter_id = plug.supplier_catalog_filter_id()
				model_name = plug.version_model()  + 'Model'
				VersionModel = getattr(model, model_name)
				query = self.session.query(SupplierCatalogModel)
				query = query.filter(SupplierCatalogModel.supplier_catalog_filter_id == supplier_catalog_filter_id)
				for supplier_catalog in query.yield_per(1):
					self.update_from_supplier_catalog(supplier_catalog, VersionModel)
					self.ts['done'] += 1
					self.session.flush()
			self.session.commit()
		except Exception:
			logger.exception('Caught Exception: ')
			if self.session.transaction is not None:
				self.session.rollback()
		finally:
			self.ts.finish()
		
		logger.debug("End update_all()")
	
	def update_from_supplier_catalog(self, supplier_catalog, VersionModel):
		self.session.begin(subtransactions=True)
		query = self.session.query(VersionModel)
		query = query.filter(VersionModel.supplier_catalog_id == supplier_catalog.id)
		query = query.filter(VersionModel.effective != supplier_catalog.issue_date)
		c = query.count()
		self.ts['sub_done'] = c
		if c > 0:
			values = dict()
			values['effective'] = supplier_catalog.issue_date
			values['updated'] = datetime.now()
			query.update(values, synchronize_session=False)
		self.session.commit()

	def vacuum(self):
		logger.debug('Begin vacuum()')
		self.vacuum_all(limit=10000)
		logger.debug('End vacuum()')
		
		
	def vacuum_all(self, limit=None):
		logger.debug('Begin vacuum_all(limit=%s)', limit)
		self.plugins = self.load_plugins()

		self.session.begin()
		
		ts = self.term_stat('SupplierCatalogItemVersion Vacuum', len(self.plugins))
		
		#s = set()
		s = ScalableBloomFilter()
		query = self.session.query(SupplierCatalogModel.id)
		for (supplier_catalog_id, ) in query.yield_per(100):
			s.add(supplier_catalog_id)
		
		
		for plug in self.plugins.itervalues():
			supplier_catalog_filter_id = plug.supplier_catalog_filter_id()
			model_name = plug.version_model()  + 'Model'
			VersionModel = getattr(model, model_name)
			query = self.session.query(VersionModel)
			if limit:
				query = query.order_by(VersionModel.vacuumed)
				query = query.limit(limit)

			ts['sub_done'] = 0
			ts['sub_total'] = query.count()
			for supplier_catalog_item_version in query.yield_per(10):
				if supplier_catalog_item_version.supplier_catalog_id not in s:
					logger.debug("Deleting %s %s", model_name, supplier_catalog_item_version.id)
					self.session.delete(supplier_catalog_item_version)
				ts['sub_done'] += 1
			ts['done'] += 1
		self.session.commit()
		ts.finish()
		logger.debug('End vacuum_all()')
