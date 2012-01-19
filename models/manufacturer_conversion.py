from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin

class ManufacturerConversion(Base, DefaultMixin):
	__tablename__ = 'manufacturer_conversions'

	manufacturer_id = Column(UUID)
	manufacturer_identifier = Column(String)
	supplier_id = Column(UUID)
