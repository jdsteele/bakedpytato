from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin

class InventoryAudit(Base, DefaultMixin):
	__tablename__ = 'inventory_audits'

	audited = Column(Date)
	inventory_audit_item_count = Column(Integer)
	name = Column(String)
	warehouse_id = Column(UUID(as_uuid=True))
