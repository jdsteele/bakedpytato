from sqlalchemy import Column, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin

class CustomerOrderIncidental(Base, DefaultMixin):
	__tablename__ = 'customer_order_incidentals'

	customer_order_id = Column(UUID)
	customer_incidental_id = Column(UUID)
	price = Column(Numeric)
