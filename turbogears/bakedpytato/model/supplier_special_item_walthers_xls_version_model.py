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

from bakedpytato.model.base_model import BaseModel, DefaultMixin
from bakedpytato.model import metadata, DBSession
from bakedpytato.model.supplier_special_item_version_mixin import SupplierSpecialItemVersionMixin

class SupplierSpecialItemWalthersXLSVersionModel(BaseModel, DefaultMixin, SupplierSpecialItemVersionMixin):
	__tablename__ = 'supplier_special_item_walthers_xls_versions'
