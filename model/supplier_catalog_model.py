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

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from model.base_model import BaseModel, DefaultMixin
import uuid

class SupplierCatalogModel(BaseModel, DefaultMixin):
	__tablename__ = 'supplier_catalogs'

	file_import_id = Column(UUID(as_uuid=True))
	#filter = Column(String)
	issue_date = Column(DateTime)
	lock_issue_date = Column(Boolean, default=False)
	next_supplier_catalog_id = Column(UUID(as_uuid=True))
	prev_supplier_catalog_id = Column(UUID(as_uuid=True))
	supplier_catalog_field_count = Column(Integer)
	supplier_catalog_item_version_count = Column(Integer)
	supplier_id = Column(UUID(as_uuid=True))
	#supplier_identifier = Column(String)
