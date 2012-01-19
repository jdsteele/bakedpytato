from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin

class SupplierCatalogItemField(Base, DefaultMixin):
	__tablename__ = 'supplier_catalog_item_fields'
