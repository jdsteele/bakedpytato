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

from sqlalchemy import Column, ForeignKey, DateTime, ForeignKey, Integer, String, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr

import uuid

class SupplierCatalogItemVersionMixin(object):

	#effective = Column(DateTime)
	#ghost = Column(Boolean, default=False)
	row_number = Column(Integer)
		
	@declared_attr
	def supplier_catalog_item_field_id(cls):
		return Column(
			UUID(as_uuid=True), 
			ForeignKey('supplier_catalog_item_fields.id')
		)

	@declared_attr
	def supplier_catalog_filter_id(cls):
		return Column(
			UUID(as_uuid=True), 
			ForeignKey('supplier_catalog_filters.id')
		)

	@declared_attr
	def supplier_catalog_id(cls):
		return Column(
			UUID(as_uuid=True), 
			ForeignKey('supplier_catalogs.id')
		)

	@declared_attr
	def supplier_catalog_item_field(cls):
		return relationship(
			'SupplierCatalogItemFieldModel'
		)

	#next_supplier_catalog_id = Column(UUID(as_uuid=True), ForeignKey('supplier_catalogs.id'))
	#prev_supplier_catalog_id = Column(UUID(as_uuid=True), ForeignKey('supplier_catalogs.id'))

	#supplier_catalog = relationship('SupplierCatalog', backref=backref('supplier_catalog_item_versions')
	#supplier_catalog_item_field = relationship('SupplierCatalogItemField')
