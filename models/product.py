from sqlalchemy import Boolean, Column, DateTime, Numeric, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin

class Product(Base, DefaultMixin):
	__tablename__ = 'products'

	archived = Column(Boolean)
	"""
	archived is True if no SupplierCatalogItems, CustomerOrderItems, 
	CustomerShipmentItems, or InventoryItems refer to this Product
	"""
	
	catalog_item_count = Column(Integer)
	category_id = Column(Integer)
	cost = Column(Numeric)
	customer_order_item_count = Column(Integer)
	customer_shipment_item_count = Column(Integer)
	description = Column(String)
	enabled = Column(Boolean)
	force_in_stock = Column(Boolean)
	identifier = Column(String)
	image_url = Column(String)
	inventory_item_count = Column(Integer)
	legacy_flag = Column(Integer)
	lock_category = Column(Boolean)
	lock_cost = Column(Boolean)
	lock_name = Column(Boolean)
	lock_retail = Column(Boolean)
	lock_sale = Column(Boolean)
	lock_scale = Column(Boolean)
	manufacturer_id = Column(UUID(as_uuid=True))
	name = Column(String)
	product_conversion_count = Column(Integer)
	product_package_count = Column(Integer)
	retail = Column(Numeric)
	sale = Column(Numeric)
	scale_id = Column(UUID(as_uuid=True))
	serial = Column(Integer)
	shippable = Column(Boolean)
	sort = Column(Integer)
	stock = Column(Numeric)
	supplier_catalog_item_count = Column(Integer)
	supplier_catalog_item_id = Column(UUID(as_uuid=True))
	supplier_phased_out = Column(Boolean)
	supplier_shipment_item_count = Column(Integer)
	url = Column(String)
