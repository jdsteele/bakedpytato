#!/usr/bin/python

#Standard Library
from datetime import date

#Extended Library

#Application Library
import cfg
from tasks import *

task = SupplierCatalogItemVersionTask()
task.update_all()


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
