from sqlalchemy import Boolean, Column, DateTime, Numeric, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from decimal import *

from base import Base, DefaultMixin

class Product(Base, DefaultMixin):
	__tablename__ = 'products'

	archived = Column(Boolean, default=False)
	"""
	archived is True if no SupplierCatalogItems, CustomerOrderItems, 
	CustomerShipmentItems, or InventoryItems refer to this Product
	"""
	
	catalog_item_count = Column(Integer, default=0)
	category_id = Column(Integer)
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
	lock_category = Column(Boolean, default=False)
	lock_cost = Column(Boolean, default=False)
	lock_name = Column(Boolean, default=False)
	lock_retail = Column(Boolean, default=False)
	lock_sale = Column(Boolean, default=False)
	lock_scale = Column(Boolean, default=False)
	manufacturer_id = Column(UUID(as_uuid=True))
	name = Column(String)
	product_conversion_count = Column(Integer, default=0)
	product_package_count = Column(Integer, default=0)
	retail = Column(Numeric, default=Decimal(0))
	sale = Column(Numeric, default=Decimal(0))
	scale_id = Column(UUID(as_uuid=True))
	serial = Column(Integer)
	shippable = Column(Boolean, default=True)
	sort = Column(Integer, default=0)
	stock = Column(Numeric, default=Decimal(0))
	supplier_advanced = Column(Boolean, default=False)
	supplier_catalog_item_count = Column(Integer, default=0)
	supplier_catalog_item_id = Column(UUID(as_uuid=True))
	supplier_phased_out = Column(Boolean, default=False)
	supplier_shipment_item_count = Column(Integer, default=0)
	supplier_special = Column(Boolean, default=False)
	supplier_stock = Column(Boolean, default=False)
	url = Column(String)
