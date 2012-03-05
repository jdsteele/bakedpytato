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

from sqlalchemy import Column, ForeignKey, DateTime, ForeignKey, Integer, String, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from bakedpytato.model import metadata, DBSession

import uuid

class SupplierSpecialItemVersionMixin(object):

	#effective = Column(DateTime)
	#ghost = Column(Boolean, default=False)
	row_number = Column(Integer)
		
	@declared_attr
	def supplier_special_item_field_id(cls):
		return Column(
			UUID(as_uuid=True), 
			ForeignKey('supplier_special_item_fields.id')
		)

	@declared_attr
	def supplier_special_filter_id(cls):
		return Column(
			UUID(as_uuid=True), 
			ForeignKey('supplier_special_filters.id')
		)

	@declared_attr
	def supplier_special_id(cls):
		return Column(
			UUID(as_uuid=True), 
			ForeignKey('supplier_specials.id')
		)

	@declared_attr
	def vacuumed(cls):
		return Column(DateTime)

	@declared_attr
	def supplier_special_item_field(cls):
		return relationship(
			'SupplierSpecialItemFieldModel'
		)

	@declared_attr
	def supplier_special(cls):
		return relationship(
			'SupplierSpecialModel'
		)
