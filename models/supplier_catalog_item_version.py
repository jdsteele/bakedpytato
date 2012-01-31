from sqlalchemy import Column, ForeignKey, DateTime, Integer, String, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from base import Base, DefaultMixin
import uuid

class SupplierCatalogItemVersion(Base, DefaultMixin):
	__tablename__ = 'supplier_catalog_item_versions'

	effective = Column(DateTime)
	ghost = Column(Boolean)
	next_supplier_catalog_id = Column(UUID(as_uuid=True))
	prev_supplier_catalog_id = Column(UUID(as_uuid=True))
	row_number = Column(Integer)
	supplier_catalog_filter_id = Column(UUID(as_uuid=True))
	supplier_catalog_id = Column(UUID(as_uuid=True))
	
	#supplier_catalog_id = Column(UUID, ForeignKey('supplier_catalogs.id'))
	#supplier_catalog_item_field_id = Column(UUID, ForeignKey('supplier_catalog_item_fields.id'))

	#supplier_catalog = relationship('SupplierCatalog', backref=backref('supplier_catalog_item_versions', order_by=DefaultMixin.id))
	#supplier_catalog_item_field = relationship('SupplierCatalogItemField', backref=backref('supplier_catalog_item_versions', order_by=DefaultMixin.id))
