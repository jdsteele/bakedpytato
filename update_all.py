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
from time import sleep

while(True):

	SupplierCatalogTask().load()
	SupplierCatalogTask().update()

	SupplierCatalogItemVersionTask().vacuum()
	SupplierCatalogItemVersionTask().load()

	SupplierCatalogItemFieldTask().vacuum()
	SupplierCatalogItemFieldTask().update()

	#SupplierCatalogItemTask().vacuum()
	SupplierCatalogItemTask().load()
	SupplierCatalogItemTask().update()
	
	#InventoryItemTask().load()
	
	#sleep(60)
	
	ProductTask().load_all()
	ProductTask().update_all()
	ProductTask().sort()

	#ProductDailyStat().load()
	#ProductWeeklyStat().load()
	#ProductMonthlyStat().load()
	#ProductYearlyStat().load()

	#ProductPackageTask.update()
	
	#CatalogTask().load()
	#CatalogCategoryTask().load()
	#CatalogTask().update()

	sleep(60*10) #10 mins
