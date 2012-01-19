from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin

class ScaleConversion(Base, DefaultMixin):
	__tablename__ = 'scale_conversions'

	scale_id = Column(UUID)
	scale_identifier = Column(String)
	supplier_id = Column(UUID)
