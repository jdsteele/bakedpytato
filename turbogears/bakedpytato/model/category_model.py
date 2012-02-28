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
### Pragma
from __future__ import unicode_literals

### Standard Library

### Extended Library
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID

### Application Library
from bakedpytato.model import metadata, DBSession
from bakedpytato.model.base_model import BaseModel, TimestampMixin


class CategoryModel(BaseModel, TimestampMixin):
	__tablename__ = 'categories'

	id = Column(Integer, primary_key=True)

