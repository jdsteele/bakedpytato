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
#Pragma
from __future__ import unicode_literals

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Numeric, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from decimal import *

from model.base_model import BaseModel, DefaultMixin

class PriceControlModel(BaseModel, DefaultMixin):
	__tablename__ = 'price_controls'

	allow_preorder = Column(Boolean)
	cost_ratio = Column(Numeric)
	enable = Column(Boolean)
	manufacturer_id = Column(UUID(as_uuid=True), ForeignKey('manufacturers.id'))
	normal = Column(Boolean)
	preorder = Column(Boolean)
	rank = Column(Integer)
	retail_ratio = Column(Numeric)
	rubber_ratio = Column(Numeric)
	retail_high = Column(Numeric, default=Decimal('inf'))
	retail_low = Column(Numeric, default=Decimal(0))
	special = Column(Boolean)
	supplier_id = Column(UUID(as_uuid=True), ForeignKey('suppliers.id'))


	def sale(self, cost, retail):
		sales = []
		sales.append(retail * (self.retail_ratio / 100))
		sales.append(cost * (self.cost_ratio / 100))
		
		#f = interp1d((0,100), (cost, retail))
		#sales.append(f(self.rubber_ratio))
		
		sales.append(
			self.linear_extrapolation(
				self.rubber_ratio,
				0,
				cost,
				100,
				retail
			)
		)
		
		sale = max(sales)
		sale = self.round(sale)
		return sale.normalize()


#*** Deprecated. use priceutil
	@classmethod
	def round(cls, value, digits=2):
		e = 10 ** digits
		value = value * e
		value = value.to_integral_value(ROUND_HALF_UP) / e
		return value


	def linear_extrapolation(self, x, xa, ya, xb, yb):
		q = xb - xa
		if (q == 0):
			return None
		
		r = x - xa
		s = yb - ya
		t = r * s
		u = t / q
		y = ya + u
		return y
