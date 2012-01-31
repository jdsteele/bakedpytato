from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin
import uuid

class SupplierCatalogFilter(Base, DefaultMixin):
	__tablename__ = 'supplier_catalog_filters'

	supplier_id = Column(UUID(as_uuid=True))
	name = Column(String)
	ghost_stock = Column(Boolean, default=False)
	ghost_phased_out = Column(Boolean, default=False)
	ghost_advanced = Column(Boolean, default=True)
