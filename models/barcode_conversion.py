from sqlalchemy import Column, Numeric, String
from sqlalchemy.dialects.postgresql import UUID

from base import Base, UUIDMixin

class BarcodeConversion(Base, UUIDMixin):
	__tablename__ = 'barcode_conversions'

	condition_1_name = Column(String)
	condition_1_value = Column(String)
	condition_2_name = Column(String)
	condition_2_value = Column(String)
	condition_3_name = Column(String)
	condition_3_value = Column(String)
	match_1 = Column(String)
	match_2 = Column(String)
	match_3 = Column(String)
	match_class = Column(String)
	multiplier = Column(Numeric)
	notes = Column(String)
	output_class = Column(String)
	regex = Column(String)
