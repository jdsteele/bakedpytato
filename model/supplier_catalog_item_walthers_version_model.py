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

from model.base_model import BaseModel, DefaultMixin
from model.supplier_catalog_item_version_mixin import SupplierCatalogItemVersionMixin

class SupplierCatalogItemWalthersVersionModel(BaseModel, DefaultMixin, SupplierCatalogItemVersionMixin):
	__tablename__ = 'supplier_catalog_item_walthers_versions'
