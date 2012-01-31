from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, UUIDMixin

class ProductBarcode(Base, UUIDMixin):
	__tablename__ = 'product_barcodes'

	product_id = Column(UUID(as_uuid=True))
	barcode = Column(String)
