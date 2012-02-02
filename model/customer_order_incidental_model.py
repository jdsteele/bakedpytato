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

from sqlalchemy import Column, ForeignKey, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID

from model.base_model import BaseModel, DefaultMixin

class CustomerOrderIncidentalModel(BaseModel, DefaultMixin):
	__tablename__ = 'customer_order_incidentals'

	customer_order_id = Column(UUID(as_uuid=True), ForeignKey('customer_orders.id'))
	customer_incidental_id = Column(UUID(as_uuid=True), ForeignKey('customer_incidentals.id'))
	price = Column(Numeric)