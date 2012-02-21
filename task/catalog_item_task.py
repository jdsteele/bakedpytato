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
#Pragma
from __future__ import unicode_literals

import logging 

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import or_, desc

from model import CatalogItemModel
from model import ManufacturerModel
from model import ProductModel
from model import SupplierCatalogItemModel

import ttystatus
import uuid
from decimal import *
from task.base_task import BaseTask

logger = logging.getLogger(__name__)

class CatalogItemTask(BaseTask):

	catalog_item_id_set = set()
	catalog_item__product_id_set = set()
	manufacturer_id_set = set()
	
	product_id_set = set()


	def init_catalog_item_cache(self):
		if len(self.catalog_item_id_set) == 0:
			query = self.session.query(CatalogItemModel)
			count = query.count()
			for catalog_item in query:
				self.catalog_item_id_set.add(catalog_item.id)
				self.catalog_item__product_id_set.add(catalog_item.product_id)


	def init_manufacturer_cache(self):
		if len(self.manufacturer_id_set) == 0:
			query = self.session.query(ManufacturerModel)
			query = query.filter(ManufacturerModel.enabled == True)
			query = query.filter(ManufacturerModel.display == True)
			for manufacturer in query:
				self.manufacturer_id_set.add(manufacturer.id)


	def init_product_cache(self):
		self.init_manufacturer_cache()
		if len(self.product_id_set) == 0:
			query = self.session.query(ProductModel)
			query = query.filter(ProductModel.enabled == True)
			query = query.filter(ProductModel.archived == False)
			query = query.filter(ProductModel.manufacturer_id.in_(self.manufacturer_id_set))
			query = query.filter(ProductModel.sale > 0)
			for product in query:
				self.product_id_set.add(product.id)


	def load_all(self):
		print "Preloading Caches..."
		self.init_product_cache()
		self.init_catalog_item_cache()
		print "Pruning..."
		self.prune()
		print "Loading...\n"
		query = self.session.query(Product)
		query = query.filter(ProductModel.enabled == True)
		query = query.filter(ProductModel.archived == False)
		query = query.filter(ProductModel.manufacturer_id.in_(self.manufacturer_id_set))
		query = query.filter(ProductModel.sale > 0)
		
		ts = ttystatus.TerminalStatus(period=0.5)
		ts.add(ttystatus.Literal('Loading Catalog Items '))
		ts.add(ttystatus.Literal(' Elapsed: '))
		ts.add(ttystatus.ElapsedTime())
		ts.add(ttystatus.Literal(' Remaining: '))
		ts.add(ttystatus.RemainingTime('done', 'total'))
		ts.add(ttystatus.Literal(' '))
		ts.add(ttystatus.PercentDone('done', 'total', decimals=2))
		ts.add(ttystatus.Literal(' '))
		ts.add(ttystatus.ProgressBar('done', 'total'))
		ts['total'] = query.count()
		ts['done'] = 0
		
		for product in query.yield_per(1000):
			self.load_one(product)
			ts['done'] += 1


	def prune(self):
		query = self.session.query(CatalogItemModel)
		for catalog_item in query:
			if catalog_item.manufacturer_id not in self.manufacturer_id_set:
				print 'Deleting By Manufacturer', catalog_item.id
				self.session.delete(catalog_item)
				self.catalog_item_id_set.discard(catalog_item.id)
				continue

			if catalog_item.product_id not in self.product_id_set:
				print 'Deleting By Product', catalog_item.id
				self.session.delete(catalog_item)
				self.catalog_item_id_set.discard(catalog_item.id)
				continue


	def load_one(self, product):
		query = self.session.query(CatalogItemModel)
		query = query.filter(CatalogItemModel.product_id == product.id)
		try:
			catalog_item = query.one()
		except NoResultFound:
			catalog_item = CatalogItemModel()

		catalog_item.set_debug(True)

		#*** From Product
		catalog_item.aacart_discount = 0
		catalog_item.category_id = product.category_id
		catalog_item.force_in_stock = product.force_in_stock
		catalog_item.phased_out = product.supplier_phased_out
		catalog_item.product_id = product.id
		catalog_item.aacart_part = product.identifier
		catalog_item.scale_id = product.scale_id
		catalog_item.sort = product.sort
		catalog_item.stock = product.stock
		catalog_item.supplier_advanced = product.supplier_advanced
		catalog_item.supplier_special = product.supplier_special
		catalog_item.supplier_stock = product.supplier_stock
		
		#*** From Manufacturer
		manufacturer = self.get_manufacturer(product.manufacturer_id)

		catalog_item.manufacturer_id = manufacturer.id
		catalog_item.aacart_man = manufacturer.identifier

		#*** From SupplierCatalogItem
		supplier_catalog_item = self.get_supplier_catalog_item(product.supplier_catalog_item_id)


	def get_manufacturer(self, manufacturer_id):
		query = self.session.query(ManufacturerModel)
		query = query.filter(ManufacturerModel.id == manufacturer_id)
		try:
			return query.one()
		except sqlalchemy.orm.exc.NoResultFound:
			return None

	def get_supplier_catalog_item(self, supplier_catalog_item_id):
		query = self.session.query(SupplierCatalogItemModel)
		query = query.filter(SupplierCatalogItemModel.id == supplier_catalog_item_id)
		try:
			return query.one()
		except NoResultFound:
			return None
