#!/usr/bin/python
import cfg
from tasks import *
from datetime import date


task = SupplierCatalogItemTask()
task.update_all()

#task = FinancialReportTask()
#task.run(date(2011,10,01), date(2011,12,31))
