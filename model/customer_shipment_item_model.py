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

from sqlalchemy import Column, ForeignKey, Boolean, Numeric, String
from sqlalchemy.dialects.postgresql import UUID

from model.base_model import BaseModel, DefaultMixin
from decimal import *

class CustomerShipmentItemModel(BaseModel, DefaultMixin):
	__tablename__ = 'customer_shipment_items'

	customer_order_item_id = Column(UUID(as_uuid=True), ForeignKey('customer_order_items.id'))
	quantity = Column(Numeric)
	void = Column(Boolean)
