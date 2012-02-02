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

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from model.base_model import BaseModel, UUIDMixin

class ProductBarcodeModel(BaseModel, UUIDMixin):
	__tablename__ = 'product_barcodes'

	product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'))
	barcode = Column(String)
