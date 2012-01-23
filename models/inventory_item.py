from sqlalchemy import Boolean, Column, DateTime, Numeric, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, UUIDMixin

class InventoryItem(Base, UUIDMixin):
	__tablename__ = 'inventory_items'

	product_id = Column(UUID(as_uuid=True))
	quantity = Column(Numeric)
	warehouse_id = Column(UUID(as_uuid=True))
	
