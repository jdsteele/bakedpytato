from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin

class CategoryConversion(Base, DefaultMixin):
	__tablename__ = 'category_conversions'

	category_id = Column(Integer)	#Yes, Integer, not UUID
	needle = Column(String)
	supplier_id = Column(UUID(as_uuid=True))
	manufacturer_id = Column(UUID(as_uuid=True))
