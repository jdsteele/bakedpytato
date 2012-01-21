from sqlalchemy import Column, Numeric, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, DefaultMixin

class ProductConversion(Base, DefaultMixin):
	__tablename__ = 'product_conversions'

	manufacturer_id = Column(UUID(as_uuid=True))
	product_id = Column(UUID(as_uuid=True))
	product_identifier = Column(String)
	source_quantity = Column(Numeric)
	target_quantity = Column(Numeric)
	supplier_id = Column(UUID(as_uuid=True))

	def get_quantity(self):
		return self.source_quantity / self.target_quantity
