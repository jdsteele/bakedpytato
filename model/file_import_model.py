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

from sqlalchemy import Boolean, Column, DateTime, Integer, String, LargeBinary
from sqlalchemy.dialects.postgresql import UUID

from model.base_model import BaseModel, DefaultMixin

class FileImportModel(BaseModel, DefaultMixin):
	__tablename__ = 'file_imports'

	content = Column(LargeBinary)
	effective = Column(DateTime)
	name = Column(String)
	size = Column(Integer)
	sha256 = Column(String(64))
	supplier_catalog_count = Column(Integer, default=0)
	mutable = Column(Boolean, default=True)
	lock_issue_date = Column(Boolean, default=False)
