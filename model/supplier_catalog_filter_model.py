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

from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from model.base_model import BaseModel, UUIDMixin

class SupplierCatalogFilterModel(BaseModel, UUIDMixin):
	__tablename__ = 'supplier_catalog_filters'

	supplier_id = Column(UUID(as_uuid=True), ForeignKey('suppliers.id'))
	name = Column(String)
	ghost_stock = Column(Boolean, default=False)
	ghost_phased_out = Column(Boolean, default=False)
	ghost_advanced = Column(Boolean, default=True)
	version_model = Column(String)
	opaque = Column(Boolean, default=True)
