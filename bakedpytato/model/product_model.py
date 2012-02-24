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

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Numeric, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from decimal import *

from model.base_model import BaseModel, DefaultMixin

class ProductModel(BaseModel, DefaultMixin):
	__tablename__ = 'products'

	archived = Column(Boolean, default=False)
	"""
	archived is True if no SupplierCatalogItems, CustomerOrderItems, 
	CustomerShipmentItems, or InventoryItems refer to this Product
	"""
	
	base_sale = Column(Numeric, default=Decimal(0))
	"""Sale price from SupplierCatalogItem before applying ratio"""
	
	catalog_item_count = Column(Integer, default=0)
	category_id = Column(Integer, ForeignKey('categories.id'))
	cost = Column(Numeric, default=Decimal(0))
	customer_order_item_count = Column(Integer, default=0)
	customer_shipment_item_count = Column(Integer, default=0)
	description = Column(String)
	enabled = Column(Boolean, default=True)
	force_in_stock = Column(Boolean, default=False)
	identifier = Column(String)
	image_url = Column(String)
	inventory_item_count = Column(Integer, default=0)
	legacy_flag = Column(Integer, default=0)
	lock_base_sale = Column(Boolean, default=False)
	lock_category = Column(Boolean, default=False)
	lock_cost = Column(Boolean, default=False)
	lock_name = Column(Boolean, default=False)
	lock_retail = Column(Boolean, default=False)
	lock_sale = Column(Boolean, default=False)
	lock_scale = Column(Boolean, default=False)
	manufacturer_id = Column(UUID(as_uuid=True), ForeignKey('manufacturers.id'))
	name = Column(String)
	product_conversion_count = Column(Integer, default=0)
	product_package_count = Column(Integer, default=0)
	ratio = Column(Numeric, default=Decimal(100))
	"""
	sale price ratio as a percent
	sale = base_sale * (ratio / 100)
	useful for applying or cancelling discounts to specific products
	"""
	
	retail = Column(Numeric, default=Decimal(0))
	sale = Column(Numeric, default=Decimal(0))
	"""Sale price from SupplierCatalogItem after applying ratio"""
	scale_id = Column(UUID(as_uuid=True), ForeignKey('scales.id'))
	serial = Column(Integer)
	shippable = Column(Boolean, default=True)
	sort = Column(Integer, default=0)
	stock = Column(Numeric, default=Decimal(0))
	supplier_advanced = Column(Boolean, default=False)
	supplier_catalog_item_count = Column(Integer, default=0)
	supplier_catalog_item_id = Column(UUID(as_uuid=True), ForeignKey('supplier_catalog_items.id'))
	supplier_phased_out = Column(Boolean, default=False)
	supplier_shipment_item_count = Column(Integer, default=0)
	supplier_special = Column(Boolean, default=False)
	supplier_stock = Column(Boolean, default=False)
	url = Column(String)
