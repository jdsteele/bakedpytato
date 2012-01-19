from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin

class CategoryConversion(Base, DefaultMixin):
	__tablename__ = 'category_conversions'

	category_id = Column(UUID)
	needle = Column(String)
	supplier_id = Column(UUID)
	manufacturer_id = Column(UUID)
