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

from sqlalchemy import Column, Numeric, String
from sqlalchemy.dialects.postgresql import UUID

from model.base_model import BaseModel, UUIDMixin

class BarcodeConversionModel(BaseModel, UUIDMixin):
	__tablename__ = 'barcode_conversions'

	condition_1_name = Column(String)
	condition_1_value = Column(String)
	condition_2_name = Column(String)
	condition_2_value = Column(String)
	condition_3_name = Column(String)
	condition_3_value = Column(String)
	match_1 = Column(String)
	match_2 = Column(String)
	match_3 = Column(String)
	match_class = Column(String)
	multiplier = Column(Numeric)
	notes = Column(String)
	output_class = Column(String)
	regex = Column(String)
