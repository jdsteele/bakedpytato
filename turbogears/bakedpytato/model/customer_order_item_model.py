# -*- coding: utf-8 -*-
"""
	BakedPotato — Inventory Management System

	BakedPotato IMS
	Copyright 2010-2012, John David Steele (john.david.steele@gmail.com)

	Licensed under The MIT License
	Redistributions of files must retain the above copyright notice.

	@copyright     Copyright 2010-2012, John David Steele (john.david.steele@gmail.com)
	@license       MIT License (http://www.opensource.org/licenses/mit-license.php)
"""
### Pragma
from __future__ import unicode_literals

### Standard Library
from decimal import Decimal

### Extended Library
from sqlalchemy import Column, ForeignKey, Boolean, Numeric, String
from sqlalchemy.dialects.postgresql import UUID

### Application Library
from bakedpytato.model import metadata, DBSession
from bakedpytato.model.base_model import BaseModel, DefaultMixin

class CustomerOrderItemModel(BaseModel, DefaultMixin):
	__tablename__ = 'customer_order_items'

	customer_order_id = Column(UUID(as_uuid=True), ForeignKey('customer_orders.id'))
	price = Column(Numeric)
	product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'))
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
