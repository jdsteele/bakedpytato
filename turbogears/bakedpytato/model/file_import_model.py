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

from sqlalchemy import Boolean, Column, DateTime, Integer, String, LargeBinary
from sqlalchemy.orm import deferred
from sqlalchemy.dialects.postgresql import UUID
import magic

from bakedpytato.model.base_model import BaseModel, DefaultMixin
from bakedpytato.model import metadata, DBSession

class FileImportModel(BaseModel, DefaultMixin):
	__tablename__ = 'file_imports'

	content = deferred(Column(LargeBinary), group='content')
	effective = Column(DateTime)
	name = Column(String)
	size = Column(Integer)
	sha256 = deferred(Column(String(64)), group='content')
	supplier_catalog_count = Column(Integer, default=0)
	mutable = Column(Boolean, default=True)
	lock_issue_date = Column(Boolean, default=False)
	
	_magic = None

	def magic(self):
		if self._magic is None:
			self._magic = dict()
			self._magic['magic'] = magic.Magic().from_buffer(self.content)
			self._magic['mime'] = magic.Magic(mime=True).from_buffer(self.content)
			self._magic['encoding'] = magic.Magic(mime_encoding=True).from_buffer(self.content)
		return self._magic
