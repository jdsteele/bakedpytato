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

from sqlalchemy import Boolean, Column, Numeric
from sqlalchemy.dialects.postgresql import UUID

from model.base_model import BaseModel, DefaultMixin

class InventoryAuditItemModel(BaseModel, DefaultMixin):
	__tablename__ = 'inventory_audit_items'

	inventory_audit_id = Column(UUID(as_uuid=True))
	product_id = Column(UUID(as_uuid=True))
	shrink = Column(Numeric)
	quantity = Column(Numeric)
	absolute = Column(Boolean)
