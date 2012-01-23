#!/usr/bin/python
import cfg
from tasks import *

task = SupplierCatalogItemTask()
task.update_all()

task = ProductTask()
task.load_all()
task.update_all()
