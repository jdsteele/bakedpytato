from sqlalchemy import Boolean, Column, DateTime, Numeric, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin

class Scale(Base, DefaultMixin):
	__tablename__ = 'scales'

	name = Column(String)
