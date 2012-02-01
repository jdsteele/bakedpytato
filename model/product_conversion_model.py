# -*- coding: utf-8 -*-
"""
	BakedPotato — Inventory Management System

	BakedPotato IMS
	Copyright 2010-2012, John David Steele (john.david.steele@gmail.com)

	Licensed under The MIT License
	Redistributions of files must retain the above copyright notice.

	@copyright     Copyright 2010-2012, John David Steele (john.david.steele@gmail.com)
	@license       MIT License (http://www.opensource.org/licenses/mit-license.php)'cmp-
"""

from sqlalchemy import Column, Numeric, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from model.base_model import BaseModel, DefaultMixin

class ProductConversionModel(BaseModel, DefaultMixin):
	__tablename__ = 'product_conversions'

	manufacturer_id = Column(UUID(as_uuid=True))
	product_id = Column(UUID(as_uuid=True))
	product_identifier = Column(String)
	source_quantity = Column(Numeric)
	target_quantity = Column(Numeric)
	supplier_id = Column(UUID(as_uuid=True))

	def get_quantity(self):
		return self.source_quantity / self.target_quantity
