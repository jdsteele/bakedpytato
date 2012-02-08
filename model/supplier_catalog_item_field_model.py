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

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import deferred
from model.base_model import BaseModel, DefaultMixin

import json
import logging 

logger = logging.getLogger(__name__)

class SupplierCatalogItemFieldModel(BaseModel, DefaultMixin):
	__tablename__ = 'supplier_catalog_item_fields'

	advanced = Column(Boolean, default = None)
	available = Column(DateTime, default=None)
	category_identifier = Column(String, default = None)
	checksum = Column(String(40), nullable=False)
	compressed = Column(Boolean, default=None)
	cost = Column(Numeric, default = None)
	fields = deferred(Column(LargeBinary), group='content')
	ghost = Column(Boolean, default=False, nullable=False)
	manufacturer_identifier = Column(String, default = None)
	name = Column(String, default = None)
	phased_out = Column(Boolean, default = None)
	product_identifier = Column(String, default = None)
	retail = Column(Numeric, default = None)
	scale_identifier = Column(String, default = None)
	special = Column(Boolean, default = None)
	special_cost = Column(Numeric, default = None)
	stock = Column(Boolean, default = None)
	supplier_catalog_item_version_count = Column(Integer, default = None)
	supplier_id = Column(UUID(as_uuid=True), ForeignKey('suppliers.id'))
	supplier_catalog_filter_id = Column(UUID(as_uuid=True), ForeignKey('supplier_catalog_filters.id'))

	def get_fields(self):
		return self.decode_json(self.fields)
	
	def set_fields(self, row):
		self.fields = self.encode_json(row)
		return self
		
	@classmethod
	def encode_json(cls, data):
		for key, value in data.iteritems():
			#value = re.sub(r'\s\s+', ' ', value)
			#value = value.strip()
			if value == "":
				value = None
				row[key] = value
				
		try:
			j = json.dumps(row, sort_keys=True, separators=(',', ':'))
			return j
		except UnicodeDecodeError:
			logger.error("UnicodeDecodeError during conversion to json:\n\t%s", row)
		return None

	@classmethod
	def decode_json(cls, j):
		try:
			return json.loads(j)
		except UnicodeDecodeError:
			logger.error("UnicodeDecodeError during conversion from json:\n\t%s", j)
		return None
