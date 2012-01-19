from sqlalchemy import Table, Boolean, Column, DateTime, Integer, Numeric, String, MetaData, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()
class Supplier(Base):
	__tablename__ = 'suppliers'

	id = Column(UUID, primary_key=True)
	name = Column(String)
	identifier = Column(String)
	created = Column(DateTime)
	modified = Column(DateTime)
	creator_id = Column(UUID)
	modifier_id = Column(UUID)
	category_conversion_count = Column(Integer)

class SupplierCatalog(Base):
	__tablename__ = 'supplier_catalogs'

	id = Column(UUID, primary_key=True)
	issue_date = Column(DateTime)
	file_import_id = Column(UUID)
	created = Column(DateTime)
	modified = Column(DateTime)
	creator_id = Column(UUID)
	modifier_id = Column(UUID)
	supplier_id = Column(UUID)
	supplier_identifier = Column(String)
	filter = Column(String)
	supplier_catalog_item_version_count = Column(Integer)
	supplier_catalog_field_count = Column(Integer)

class SupplierCatalogItem(Base):
	__tablename__ = 'supplier_catalog_items'

	id = Column(UUID, primary_key=True)

class SupplierCatalogItemVersion(Base):
	__tablename__ = 'supplier_catalog_item_versions'

	id = Column(UUID, primary_key=True)
	supplier_catalog_id = Column(UUID, ForeignKey('supplier_catalogs.id'))
	supplier_catalog_field_id = Column(UUID)

	name = Column(String)
	product_identifier = Column(String)
	manufacturer_identifier = Column(String)
	cost = Column(Numeric)
	retail = Column(Numeric)
	row_number = Column(Integer)
	stock = Column(Boolean)
	scale_identifier = Column(String)
	category_identifier = Column(String)
	created = Column(DateTime)
	modified = Column(DateTime)
	ghost = Column(Boolean)
	phased_out = Column(Boolean)
	special = Column(Boolean)

	supplier_catalog = relationship('SupplierCatalog', backref=backref('supplier_catalog_item_versions', order_by=id))
	#supplier_catalog_field = relationship('SupplierCatalogField', backref=backref('supplier_catalog_item_versions', order_by=id))
