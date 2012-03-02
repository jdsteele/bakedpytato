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
from decimal import Decimal
import transaction
from datetime import datetime, timedelta

### Extended Library
import ttystatus
from sqlalchemy import or_, desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

### Application Library
from bakedpytato import cfg
from bakedpytato.model import DBSession
from bakedpytato.model import CustomerOrderItemModel, CustomerShipmentItemModel
from bakedpytato.model import InventoryItemModel
from bakedpytato.model import ManufacturerModel
from bakedpytato.model import ProductModel
from bakedpytato.model import SupplierCatalogItemModel
from bakedpytato.task.base_task import BaseTask
from bakedpytato.task.supplier_catalog_item_task import SupplierCatalogItemTask
from bakedpytato.util.price_util import decimal_psych_price
from bakedpytato.util.sort_util import alphanum_key


logger = logging.getLogger(__name__)

class ProductTask(BaseTask):

	def load(self):
		self.load_all()
		
	def load_all(self):
		"""Load All"""
		logger.debug("Begin load_all()")
		tx = transaction.get()
		try:
			query = DBSession.query(SupplierCatalogItemModel)
			query = query.filter(SupplierCatalogItemModel.manufacturer_identifier != None)
			query = query.filter(SupplierCatalogItemModel.manufacturer_id != None)
			query = query.filter(SupplierCatalogItemModel.product_identifier != None)
			query = query.filter(SupplierCatalogItemModel.product_id == None)
			query = query.filter(SupplierCatalogItemModel.category_id != None)
			query = query.filter(SupplierCatalogItemModel.scale_id != None)
			query = query.filter(SupplierCatalogItemModel.phased_out == False)
			query = query.filter(
				or_(
					SupplierCatalogItemModel.in_stock == True,
					SupplierCatalogItemModel.advanced == True
				)
			)
			ts = self.term_stat('Products Load', query.count())

			for supplier_catalog_item in query.yield_per(1000):
				self.load_one(supplier_catalog_item)
				ts['done'] += 1
		except Exception:
			logger.exception("Caught Exception: ")
			tx.abort()
		finally:
			ts.finish()
		logger.debug("End load_all()")


	def load_one(self, supplier_catalog_item):
		"""Load One"""
		query = DBSession.query(ProductModel)
		query = query.filter(ProductModel.manufacturer_id == supplier_catalog_item.manufacturer_id)
		query = query.filter(ProductModel.identifier == supplier_catalog_item.product_identifier)
		count = query.count()
		
		if (count == 0):
			product = ProductModel()
			product.manufacturer_id = supplier_catalog_item.manufacturer_id
			product.identifier = supplier_catalog_item.product_identifier
			DBSession.add(product)
			
			supplier_catalog_item_task = SupplierCatalogItemTask()
			supplier_catalog_item_task.update_product(supplier_catalog_item)


	def update(self):
		self.update_all(limit=10000, time_limit=timedelta(hours=1))


	def update_all(self, limit, time_limit):
		"""Update All"""
		logger.debug("Begin update_all()")
		ts = self.term_stat('Products Update')
		start_time = datetime.now()
		tx = transaction.get()
		try:
			query = DBSession.query(ProductModel)
			if limit is not None:
				query = query.order_by(ProductModel.updated.nullsfirst())
				query = query.limit(limit)

			ts['total'] = query.count()

			for product in query.yield_per(100):
				self.update_one(product)
				if ts['done'] % 100 == 0:
					DBSession.flush()
				if time_limit is not None:
					if datetime.now() > start_time + time_limit:
						logger.info("Reached Time Limit at %i of %i", ts['done'], ts['total'])
						break;
				ts['done'] += 1
		except Exception:
			logger.exception("Caught Exception: ")
			tx.abort()
		finally:
			ts.finish()
		logger.debug("End update_all()")


	def update_one(self, product):
		"""Update One"""
		
		##FIXME add code for 
		#	supplier_shipment_item_count
		#	product_conversion_count
		#	product_package_count
		#	catalog_item_count
		
		self.update_supplier_catalog_items(product)
		self.update_inventory_items(product)
		self.update_customer_order_items(product)
		if (
			product.supplier_catalog_item_count > 0 or
			product.customer_order_item_count > 0 or
			product.customer_shipment_item_count > 0 or
			product.inventory_item_count > 0 or
			product.force_in_stock == True
		):
			product.archived = False
		else:
			product.archived = True
		if product.lock_sale is False and product.base_sale > Decimal(0):
			sale = product.base_sale * (product.ratio / Decimal(100))
			product.sale = decimal_psych_price(sale, cfg.sale_decimals)
		product.updated = datetime.now()

	def sort(self):
		try:
			logger.info("Caching Manufacturers...")
			manufacturers = dict()
			query = DBSession.query(ManufacturerModel)
			for manufacturer in query:
				manufacturers[manufacturer.id] = manufacturer.name

			query = DBSession.query(ProductModel)
			query = query.order_by(ProductModel.sort)
			
			sorttable = list()
			
			logger.info("Generating List...")
			
			for product in query:
				data = [
					product.id, 
					manufacturers[product.manufacturer_id], 
					product.identifier
				]
				sorttable.append(data)
			
			def sortkey(s):
				return (alphanum_key(s[1]), alphanum_key(s[2]))
			
			
			logger.info("Sorting List...")
			sorttable.sort(key=sortkey)

			ts = self.term_stat('Products Sort', len(sorttable))

			for x in xrange(len(sorttable)):
				(product_id, a, b) = sorttable[x]
				query = DBSession.query(ProductModel)
				#query = query.filter(ProductModel.id == product_id)
				#product = query.one()
				product = query.get(product_id)
				product.sort = x
				ts['done'] += 1
		except Exception:
			logger.exception("Caught Exception: ")
			transaction.abort()
		finally:
			ts.finish()

	def update_supplier_catalog_items(self, product):
		"""Update Supplier Catalog Items"""
		data = self.get_supplier_catalog_item(product)
		
		#product.set_debug(True)
		
		product.supplier_catalog_item_count = data['supplier_catalog_item_count']
		product.supplier_phased_out = data['phased_out']
		product.supplier_stock = data['in_stock']
		product.supplier_advanced = data['advanced']

		if (not product.lock_scale) and (data['scale_id'] is not None):
			product.scale_id = data['scale_id']
		if (not product.lock_category) and (data['category_id'] is not None):
			product.category_id = data['category_id']

		supplier_catalog_item = data['supplier_catalog_item']
		if supplier_catalog_item is not None:
			if product.lock_name is False:
				product.name = supplier_catalog_item.name
			if product.lock_cost is False:
				product.cost = supplier_catalog_item.cost
			if product.lock_retail is False:
				product.retail = supplier_catalog_item.retail
			if product.lock_base_sale is False:
				product.base_sale = supplier_catalog_item.sale
			product.supplier_catalog_item_id = supplier_catalog_item.id
			product.supplier_special = supplier_catalog_item.special

		else:
			product.supplier_catalog_item_id = None
			product.supplier_special = False


	def update_inventory_items(self, product):
		"""Update Inventory Items"""
		query = DBSession.query(InventoryItemModel)
		query = query.filter(InventoryItemModel.product_id == product.id)
		product.inventory_item_count = query.count()
		
		quantity = Decimal(0)
		
		for inventory_item in query:
			quantity += inventory_item.quantity
		
		product.stock = quantity


	def update_customer_order_items(self, product):
		"""Update Customer Order Items"""
		query = DBSession.query(CustomerOrderItemModel)
		query = query.filter(CustomerOrderItemModel.product_id == product.id)
		product.customer_order_item_count = query.count()

		for customer_order_item in query:
			query2 = DBSession.query(CustomerShipmentItemModel)
			query2 = query.filter(CustomerShipmentItemModel.customer_order_item_id == customer_order_item.id)
			product.customer_shipment_item_count = query2.count()


	def get_supplier_catalog_item(self, product):
		"""Get Supplier Catalog Item"""
		#print "Product", product.id
		data = dict()
		
		data['phased_out'] = False
		data['in_stock'] = False
		data['advanced'] = False
		data['supplier_catalog_item'] = None
		data['category_id'] = None
		data['scale_id'] = None
		
		query = DBSession.query(SupplierCatalogItemModel)
		query = query.filter(SupplierCatalogItemModel.product_id == product.id)
		query = query.filter(SupplierCatalogItemModel.rank > 0)
		query.order_by(asc(SupplierCatalogItemModel.rank))
		
		count = data['supplier_catalog_item_count'] = query.count()
		
		if count == 0:
			return data
	
		supplier_catalog_items = query.all()
		
		#*** Find SCI with highest rank having product in stock
		for supplier_catalog_item in supplier_catalog_items:
			#print "SCI", supplier_catalog_item.id
			
			if supplier_catalog_item.phased_out is True:
				data['phased_out'] = True
			if supplier_catalog_item.in_stock is True:
				data['in_stock'] = True
				data['supplier_catalog_item'] = supplier_catalog_item
			if supplier_catalog_item.category_id is not None:
				data['category_id'] = supplier_catalog_item.category_id
			if supplier_catalog_item.scale_id is not None:
				data['scale_id'] = supplier_catalog_item.scale_id
			
		
		if data['in_stock']:
			return data

		#*** Find SCI with highest rank having product on pre-order
		for supplier_catalog_item in supplier_catalog_items:
			#print "SCI", supplier_catalog_item.id
			
			if supplier_catalog_item.advanced is True:
				data['advanced'] = True
				data['supplier_catalog_item'] = supplier_catalog_item

		if data['advanced']:
			return data
		
		#*** since no supplier has stock, or advanced orders
		#*** we return the SCI with the highest rank
		data['supplier_catalog_item'] = supplier_catalog_items[-1]
		return data

