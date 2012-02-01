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
import logging 
import uuid
from decimal import *

#Extended Library
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import or_, desc
import ttystatus

#Application Library
from model import CustomerOrderItemModel, CustomerShipmentItemModel
from model import InventoryItemModel
from model import ManufacturerModel
from model import ProductModel
from model import SupplierCatalogItemModel
from priceutil import decimal_psych_price
import cfg
import sortutil

#This Package
from task.base_task import BaseTask
from task.supplier_catalog_item_task import SupplierCatalogItemTask

logger = logging.getLogger(__name__)

class ProductTask(BaseTask):

	def load_all(self):
		"""Load All"""
		logger.debug("Begin load_all()")
		query = self.session.query(SupplierCatalogItemModel)
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

		ts = ttystatus.TerminalStatus(period=0.5)
		ts.add(ttystatus.Literal('Loading Products '))
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

		self.session.begin()
		for supplier_catalog_item in query.yield_per(1000):
			self.load_one(supplier_catalog_item)
			self.session.flush()
			ts['done'] += 1
		ts.clear()
		ts.add(ttystatus.Literal(' Committing '))
		ts.add(ttystatus.ElapsedTime())
		self.session.commit()
		ts.finish()
		logger.debug("End load_all()")


	def load_one(self, supplier_catalog_item):
		"""Load One"""
		
		query = self.session.query(ProductModel)
		query = query.filter(ProductModel.manufacturer_id == supplier_catalog_item.manufacturer_id)
		query = query.filter(ProductModel.identifier == supplier_catalog_item.product_identifier)
		count = query.count()
		
		if (count == 0):
			product = ProductModel()
			product.manufacturer_id = supplier_catalog_item.manufacturer_id
			product.identifier = supplier_catalog_item.product_identifier
			self.session.add(product)
			
			supplier_catalog_item_task = SupplierCatalogItemTask()
			supplier_catalog_item_task.update_one(supplier_catalog_item)
		
	def update_all(self):
		"""Update All"""
		logger.debug("Begin update_all()")
		query = self.session.query(ProductModel)

		ts = ttystatus.TerminalStatus(period=0.5)
		ts.add(ttystatus.Literal('Updating Products '))
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

		self.session.begin()
		for product in query.yield_per(1000):
			self.update_one(product)
			self.session.flush()
			ts['done'] += 1
		ts.clear()
		ts.add(ttystatus.Literal(' Committing '))
		ts.add(ttystatus.ElapsedTime())
		self.session.commit()
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

	def sort(self):
		print "Caching Manufacturers..."
		manufacturers = dict()
		query = self.session.query(ManufacturerModel)
		for manufacturer in query:
			manufacturers[manufacturer.id] = manufacturer.name

		query = self.session.query(ProductModel)
		query = query.order_by(ProductModel.sort)
		
		sorttable = list()
		
		print "Generating List..."
		
		for product in query:
			data = [
				product.id, 
				manufacturers[product.manufacturer_id], 
				product.identifier
			]
			sorttable.append(data)
		
		def sortkey(s):
			return (sortutil.alphanum_key(s[1]), sortutil.alphanum_key(s[2]))
		
		
		print "Sorting List..."
		sorttable.sort(key=sortkey)

		ts = ttystatus.TerminalStatus(period=0.5)
		ts.add(ttystatus.Literal('Sorting Products '))
		ts.add(ttystatus.Literal(' Elapsed: '))
		ts.add(ttystatus.ElapsedTime())
		ts.add(ttystatus.Literal(' Remaining: '))
		ts.add(ttystatus.RemainingTime('done', 'total'))
		ts.add(ttystatus.Literal(' '))
		ts.add(ttystatus.PercentDone('done', 'total', decimals=2))
		ts.add(ttystatus.Literal(' '))
		ts.add(ttystatus.ProgressBar('done', 'total'))
		ts['total'] = len(sorttable)
		ts['done'] = 0

		for x in xrange(len(sorttable)):
			(product_id, a, b) = sorttable[x]
			query = self.session.query(ProductModel)
			query = query.filter(ProductModel.id == product_id)
			product = query.one()
			self.session.begin()
			product.sort = x
			self.session.commit()
			ts['done'] += 1

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
		query = self.session.query(InventoryItemModel)
		query = query.filter(InventoryItemModel.product_id == product.id)
		product.inventory_item_count = query.count()
		
		quantity = Decimal(0)
		
		for inventory_item in query:
			quantity += inventory_item.quantity
		
		product.stock = quantity


	def update_customer_order_items(self, product):
		"""Update Customer Order Items"""
		query = self.session.query(CustomerOrderItemModel)
		query = query.filter(CustomerOrderItemModel.product_id == product.id)
		product.customer_order_item_count = query.count()

		for customer_order_item in query:
			query2 = self.session.query(CustomerShipmentItemModel)
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
		
		query = self.session.query(SupplierCatalogItemModel)
		query = query.filter(SupplierCatalogItemModel.product_id == product.id)
		query = query.filter(SupplierCatalogItemModel.rank > 0)
		query.order_by(desc(SupplierCatalogItemModel.rank))
		
		count = data['supplier_catalog_item_count'] = query.count()
		
		if count == 0:
			return data
		
		supplier_catalog_items = (query)
		
		#*** Find SCI with highest rank having product in stockchilm
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

