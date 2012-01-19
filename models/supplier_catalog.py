from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin
import uuid

class SupplierCatalog(Base, DefaultMixin):
	__tablename__ = 'supplier_catalogs'

	file_import_id = Column(UUID)
	filter = Column(String)
	issue_date = Column(DateTime)
	next_supplier_catalog_id = Column(UUID)
	supplier_catalog_field_count = Column(Integer)
	supplier_catalog_item_version_count = Column(Integer)
	supplier_id = Column(UUID)
	supplier_identifier = Column(String)
