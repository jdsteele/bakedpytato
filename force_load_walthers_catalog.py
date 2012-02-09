#!/usr/bin/python
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

import cfg
from task import *

while(True):

	#SupplierCatalogTask().load_all()
	#SupplierCatalogTask().update_all()

	SupplierCatalogItemVersionTask().load_all(
		supplier_id='4e8cfc8d-fa9c-4416-92e0-541066c1c7e4', 
		item_versions_loaded=False
	)

	#SupplierCatalogItemFieldTask().update_all()

	#SupplierCatalogItemVersionTask().update_all()

	#SupplierCatalogItemTask().load()
	#SupplierCatalogItemTask().update()
	
	#ProductTask().load_all()
	#ProductTask().update_all()
	#ProductTask().sort()
