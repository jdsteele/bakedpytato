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

from sqlalchemy import Column, ForeignKey, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from model.base_model import BaseModel, DefaultMixin

class CategoryConversionModel(BaseModel, DefaultMixin):
	__tablename__ = 'category_conversions'

	category_id = Column(Integer, ForeignKey('categories.id'))	#Yes, Integer, not UUID
	needle = Column(String)
	supplier_id = Column(UUID(as_uuid=True), ForeignKey('suppliers.id'))
	manufacturer_id = Column(UUID(as_uuid=True), ForeignKey('manufacturers.id'))
