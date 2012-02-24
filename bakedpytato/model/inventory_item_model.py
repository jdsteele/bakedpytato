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

from sqlalchemy import Boolean, Column, ForeignKey, DateTime, Numeric, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from model.base_model import BaseModel, UUIDMixin

class InventoryItemModel(BaseModel, UUIDMixin):
	__tablename__ = 'inventory_items'

	product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'))
	quantity = Column(Numeric)
	warehouse_id = Column(UUID(as_uuid=True), ForeignKey('warehouses.id'))
	
