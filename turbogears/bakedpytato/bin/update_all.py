#!/usr/bin/env python
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

from time import sleep

import os
import sys
import subprocess
from argparse import ArgumentParser


#def load_config(filename):
    #conf = appconfig('config:' + os.path.abspath(filename))
    #load_environment(conf.global_conf, conf.local_conf)

def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("conf_file", help="configuration to use")
    return parser.parse_args()

def main():
	args = parse_args()
	#load_config(args.conf_file)
	
	cmd = 'bakedpytato/bin/runner.py'
	
	tasks = [
		['SupplierCatalogTask', 'load'],
		['SupplierCatalogTask', 'update'],
		['SupplierCatalogItemVersionTask', 'load'],
		['SupplierCatalogItemVersionTask', 'vacuum'],
		['SupplierCatalogItemFieldTask', 'update'],
		['SupplierCatalogItemFieldTask', 'vacuum'],
		['SupplierCatalogItemTask', 'load'],
		['SupplierCatalogItemTask', 'update'],
		#['SupplierCatalogItemTask', 'vacuum'],
		#['InventoryItemTask', 'load'],
		['ProductTask', 'load'],
		['ProductTask', 'update'],
		['ProductTask', 'sort'],

		##task.ProductDailyStat().load()
		##task.ProductWeeklyStat().load()
		##task.ProductMonthlyStat().load()
		##task.ProductYearlyStat().load()

		##task.ProductPackageTask.update()
		
		##task.CatalogTask().load()
		##task.CatalogCategoryTask().load()
		##task.CatalogTask().update()
	]

	while(True):
		
		for (task_name, method_name) in tasks:
			subprocess.call(['python2.6', cmd, args.conf_file, task_name, method_name])
		

		print "Sleep..."
		sleep(60*10) #10 mins

if __name__ == '__main__':
    sys.exit(main())
