#!/usr/bin/python
# -*- coding: utf-8 -*-

#Standard Library
#from datetime import date

#Extended Library

#Application Library
import cfg
from task import *
#from plugin import *
#from model import *

task = SupplierCatalogTask()
task.load_all()
#task.update_all()

#task = SupplierCatalogItemVersionTask()
#task.update_all()


#task = SupplierCatalogItemTask()
#task.update_all()

#task = ProductTask()
#task.load_all()
#task.update_all()
#task.sort()

#task = CatalogItemTask()
#task.load_all()

#task = FinancialReportTask()
#task.run(date(2011,10,01), date(2011,12,31))

#task = SupplierCatalogItemFieldTask()
#task.update_all()
