from sqlalchemy import Column, DateTime, Boolean, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin

class CustomerOrder(Base, DefaultMixin):
	__tablename__ = 'customer_orders'

	ordered = Column(DateTime)
	closed = Column(DateTime)
	void = Column(Boolean)
	identifier = Column(String)
