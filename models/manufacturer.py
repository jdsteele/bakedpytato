from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin

class Manufacturer(Base, DefaultMixin):
	__tablename__ = 'manufacturers'

	display = Column(Boolean)
	enabled = Column(Boolean)
	identifier = Column(String)
	name = Column(String)

