from sqlalchemy import Column, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin

class CustomerIncidental(Base, DefaultMixin):
	__tablename__ = 'customer_incidentals'

	name = Column(String)
