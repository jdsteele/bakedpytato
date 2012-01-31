#!/usr/bin/python
import cfg
from tasks import *

task = SupplierCatalogTask()
task.update_all()

#task = SupplierCatalogItemVersionTask()
#task.update_all()

task = SupplierCatalogItemTask()
task.update_all()

task = ProductTask()
task.load_all()
task.update_all()
task.sort()
