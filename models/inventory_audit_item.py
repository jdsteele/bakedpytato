from sqlalchemy import Boolean, Column, Numeric
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin

class InventoryAuditItem(Base, DefaultMixin):
	__tablename__ = 'inventory_audit_items'

	inventory_audit_id = Column(UUID(as_uuid=True))
	product_id = Column(UUID(as_uuid=True))
	shrink = Column(Numeric)
	quantity = Column(Numeric)
	absolute = Column(Boolean)
