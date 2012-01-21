from sqlalchemy import Boolean, Column, DateTime, Numeric, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin

class Product(Base, DefaultMixin):
	__tablename__ = 'products'

	identifier = Column(String)
	manufacturer_id = Column(UUID(as_uuid=True))
	name = Column(String)
