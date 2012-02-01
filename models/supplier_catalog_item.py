from sqlalchemy import event
from sqlalchemy import Column, Boolean, DateTime, Numeric, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin



class SupplierCatalogItem(Base, DefaultMixin):
	__tablename__ = 'supplier_catalog_items'

	advanced = Column(Boolean, default=False)
	category_id = Column(Integer)
	category_identifier = Column(String)
	
	cost = Column(Numeric, default=0.0)
	"""cost per unit"""
	
	in_stock = Column(Boolean, default=False)
	manufacturer_id = Column(UUID(as_uuid=True))
	manufacturer_identifier = Column(String)
	name = Column(String)
	phased_out = Column(Boolean, default=False)
	price_control_id = Column(UUID(as_uuid=True))
	product_id = Column(UUID(as_uuid=True))
	product_identifier = Column(String)
	quantity = Column(Numeric, default=1)
	"""ratio (supplier unit/unit)"""
	
	quantity_cost = Column(Numeric, default=0.0)
	"""cost price of a supplier unit"""
	
	quantity_retail = Column(Numeric, default=0.0)
	"""retail price of a supplier_unit"""

	quantity_special_cost = Column(Numeric, default=0.0)
	"""cost price of a supplier unit during special"""
	
	rank = Column(Integer, default=0)
	retail = Column(Numeric, default=0.0)
	"""retail price per unit"""
	
	sale = Column(Numeric, default=0.0)
	"""sale price per unit as generated by PriceControl"""
	
	scale_id = Column(UUID(as_uuid=True))
	scale_identifier = Column(String)
	special = Column(Boolean, default=False)
	"""item is on temorary supplier discount AKA 'sale' or 'special'"""
	
	special_cost = Column(Numeric, default=0.0)
	"""cost per unit during special"""
	supplier_id = Column(UUID(as_uuid=True))

