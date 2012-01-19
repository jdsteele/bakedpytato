from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base

class Supplier(Base):
	__tablename__ = 'suppliers'

	id = Column(UUID, primary_key=True)
	name = Column(String)
	identifier = Column(String)
	category_conversion_count = Column(Integer)
