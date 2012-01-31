from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin

class Supplier(Base, DefaultMixin):
	__tablename__ = 'suppliers'

	name = Column(String)
	identifier = Column(String)
	category_conversion_count = Column(Integer)
