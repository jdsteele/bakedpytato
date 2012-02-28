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

### Extended Library
from sqlalchemy import Column, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID

### Application Library
from bakedpytato.model import metadata, DBSession
from bakedpytato.model.base_model import BaseModel, DefaultMixin

class CustomerIncidentalModel(BaseModel, DefaultMixin):
	__tablename__ = 'customer_incidentals'

	name = Column(String)
