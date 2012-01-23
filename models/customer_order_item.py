from sqlalchemy import Column, Boolean, Numeric, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin
from decimal import *

class CustomerOrderItem(Base, DefaultMixin):
	__tablename__ = 'customer_order_items'

	customer_order_id = Column(UUID(as_uuid=True))
	price = Column(Numeric)
	product_id = Column(UUID(as_uuid=True))
	quantity = Column(Numeric)
	void = Column(Boolean)
	
	def extended(self):
		if self.price is None:
			return Decimal(0)
		if self.quantity is None:
			return Decimal(0)
		return self.round(self.price * self.quantity)

	@classmethod
	def round(cls, value, digits=2):
		e = 10 ** digits
		value = value * e
		value = value.to_integral_value(ROUND_HALF_UP) / e
		return value
