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

from sqlalchemy import Boolean, Column, DateTime, Numeric, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from model.base_model import BaseModel, DefaultMixin

class CatalogItemModel(BaseModel, DefaultMixin):
	__tablename__ = 'catalog_items'

	aacart_discount = Column(Integer)
	aacart_man = Column(String)
	aacart_part = Column(String)
	category_id = Column(Integer)
	force_in_stock = Column(Boolean)
	manufacturer_id = Column(UUID(as_uuid=True))
	phased_out = Column(Boolean)
	product_id = Column(UUID(as_uuid=True))
	scale_id = Column(UUID(as_uuid=True))
	sort = Column(Integer)
	stock = Column(Numeric)
	supplier_advanced = Column(Boolean)
	supplier_special = Column(Boolean)
	supplier_stock = Column(Boolean)
	
