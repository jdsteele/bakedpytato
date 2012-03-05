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

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from bakedpytato.model.base_model import BaseModel, DefaultMixin
from bakedpytato.model import metadata, DBSession
import uuid

class SupplierSpecialModel(BaseModel, DefaultMixin):
	__tablename__ = 'supplier_specials'

	file_import_id = Column(UUID(as_uuid=True), ForeignKey('file_imports.id'))
	begin_date = Column(Date)
	end_date = Column(Date)
	supplier_special_filter_id = Column(UUID(as_uuid=True), ForeignKey('supplier_special_filters.id'))
	supplier_special_item_versions_loaded = Column(DateTime)
	supplier_id = Column(UUID(as_uuid=True), ForeignKey('suppliers.id'))

# *** Relations

	file_import = relationship("FileImportModel", backref=backref('supplier_specials'))
