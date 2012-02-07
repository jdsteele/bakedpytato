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
import hashlib
import json
import logging 
import re

#Extended Library
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import desc

#Application Library
import model
from model import SupplierCatalogItemVersionModel
from model import SupplierCatalogItemFieldModel
from model import SupplierCatalogModel

#This Package
from task.base_supplier_catalog_task import BaseSupplierCatalogTask

logger = logging.getLogger(__name__)

class SupplierCatalogItemVersionTask(BaseSupplierCatalogTask):
	
	def load(self):
		"""Load"""
		logger.debug("Begin load()")
		self.plugins = self.load_plugins()
		query = self.session.query(SupplierCatalogModel)
		query = query.filter(SupplierCatalogModel.item_versions_loaded == False)
		query = query.order_by(desc(SupplierCatalogModel.issue_date))
		if query.count() > 0:
			supplier_catalog = query.first()
			self.ts = self.term_stat('SupplierCatalogItemVersion Load', query.count())
			logger.info("Loading ItemVersions for SupplierCatalog %s", supplier_catalog.id)
			self.load_from_supplier_catalog(supplier_catalog)
			self.session.begin(subtransactions=True)
			supplier_catalog.item_versions_loaded = True
			self.session.commit()
		else:
			logger.info("No Unloaded SupplierCatalogs Found")
			## TODO: re-load a randomly picked catalog here?
		logger.debug("End load()")
	
	def load_all(self):
		"""Load All"""
		logger.debug("Begin load_all()")
		self.plugins = self.load_plugins()
		query = self.session.query(SupplierCatalogModel)
		self.ts = self.term_stat('SupplierCatalogItemVersion Load All', query.count())
		for supplier_catalog in query.yield_per(10):
			self.load_one(supplier_catalog)
			self.ts['done'] += 1
		self.ts.finish()
		logger.debug("End load_all()")
		
	def load_one(self, supplier_catalog):
		self.sesion.begin(subtransactions=True)
		self.load_from_supplier_catalog(supplier_catalog)
		self.sesion.commit()
			
	def load_from_supplier_catalog(self, supplier_catalog):
		self.session.begin(subtransactions=True)

		if not supplier_catalog.supplier_catalog_filter_id in self.plugins:
			logger.warning("Plugin %s Not Found", supplier_catalog.supplier_catalog_filter_id)
			return None
		plug = self.plugins[supplier_catalog.supplier_catalog_filter_id]
		self.ts['sub_done'] = 0
		row_number = 0

		for row in plug.get_items(supplier_catalog):
			self.ts['sub_done'] += 1
			row_number += 1
			for key, value in row.iteritems():
				#value = re.sub(r'\s\s+', ' ', value)
				#value = value.strip()
				if value == "":
					value = None
				row[key] = value
				
			try:
				j = json.dumps(row, sort_keys=True, separators=(',', ':'))
				#print j
			except UnicodeDecodeError:
				logger.error("UnicodeDecodeError during conversion to json:\n\t%s", row)
				continue
			supplier_catalog_item_field = self.load_supplier_catalog_item_field(supplier_catalog, j)
			self.load_supplier_catalog_item_version(supplier_catalog, supplier_catalog_item_field, row_number)
		self.session.commit()

	def load_supplier_catalog_item_field(self, supplier_catalog, j):
		self.session.begin(subtransactions=True)
		plug = self.plugins[supplier_catalog.supplier_catalog_filter_id]
		checksum = hashlib.sha1(j).hexdigest()
		
		query = self.session.query(SupplierCatalogItemFieldModel)
		query = query.filter(SupplierCatalogItemFieldModel.checksum == checksum)
		try:
			supplier_catalog_item_field = query.one()
		except NoResultFound:
			supplier_catalog_item_field = SupplierCatalogItemFieldModel()
			self.session.add(supplier_catalog_item_field)
		
		supplier_catalog_item_field.fields = j
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
		supplier_catalog_item_version.ghost = False
		self.session.commit()


	def update_all(self):
		logger.debug("Begin update_all()")
		self.session.begin(subtransactions=True)
		query = self.session.query(SupplierCatalogModel)

		ts = self.term_stat("Updating SCIV From SC", query.count())
		for supplier_catalog in query:
			self.update_from_supplier_catalog(supplier_catalog)
			ts['done'] += 1
		ts.finish()
		self.session.commit()
		logger.debug("End update_all()")
	
	def update_from_supplier_catalog(self, supplier_catalog):
		self.session.begin(subtransactions=True)
		query = self.session.query(SupplierCatalogItemVersionModel)
		query = query.filter(SupplierCatalogItemVersionModel.supplier_catalog_id == supplier_catalog.id)

		values = dict()
		values['prev_supplier_catalog_id'] = supplier_catalog.prev_supplier_catalog_id
		values['next_supplier_catalog_id'] = supplier_catalog.next_supplier_catalog_id
		values['effective'] = supplier_catalog.issue_date
		query.update(values, synchronize_session=False)
		self.session.commit()
