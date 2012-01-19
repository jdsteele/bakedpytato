from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin

class Manufacturer(Base, DefaultMixin):
	__tablename__ = 'manufacturers'

	identifier = Column(String)
	name = Column(String)
