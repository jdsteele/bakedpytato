#!/usr/bin/python
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

import cfg
from task import *

while(True):

	task = SupplierCatalogTask()
	task.load_all()
	task.update_all()

	##task = SupplierCatalogItemVersionTask()
	##task.load_all()
	##task.update_all()

	##task = SupplierCatalogItemFieldTask()
	##task.load_all()
	##task.update_all()


	task = SupplierCatalogItemTask()
	##task.load_all()
	task.update_all()

	task = ProductTask()
	task.load_all()
	task.update_all()
	task.sort()
