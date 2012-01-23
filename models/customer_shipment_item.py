from sqlalchemy import Column, Boolean, Numeric, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin
from decimal import *

class CustomerShipmentItem(Base, DefaultMixin):
	__tablename__ = 'customer_shipment_items'

	customer_order_item_id = Column(UUID(as_uuid=True))
	quantity = Column(Numeric)
	void = Column(Boolean)
