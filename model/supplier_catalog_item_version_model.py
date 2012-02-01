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

from sqlalchemy import Column, ForeignKey, DateTime, Integer, String, Numeric, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from model.base_model import BaseModel, DefaultMixin
import uuid

class SupplierCatalogItemVersionModel(BaseModel, DefaultMixin):
	__tablename__ = 'supplier_catalog_item_versions'

	effective = Column(DateTime)
	ghost = Column(Boolean)
	next_supplier_catalog_id = Column(UUID(as_uuid=True))
	prev_supplier_catalog_id = Column(UUID(as_uuid=True))
	row_number = Column(Integer)
	supplier_catalog_filter_id = Column(UUID(as_uuid=True))
	supplier_catalog_id = Column(UUID(as_uuid=True))
	
	#supplier_catalog_id = Column(UUID, ForeignKey('supplier_catalogs.id'))
	#supplier_catalog_item_field_id = Column(UUID, ForeignKey('supplier_catalog_item_fields.id'))

	#supplier_catalog = relationship('SupplierCatalog', backref=backref('supplier_catalog_item_versions', order_by=DefaultMixin.id))
	#supplier_catalog_item_field = relationship('SupplierCatalogItemField', backref=backref('supplier_catalog_item_versions', order_by=DefaultMixin.id))
