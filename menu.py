#!/usr/bin/python
import cfg
#from tasks import *
import tasks
from datetime import date

task_list = []

for v in sorted(vars(tasks).iterkeys()):
	if v.endswith('Task'):
		tasklist.append(v)




#task = SupplierCatalogItemTask()
#task.update_all()

#Task = literal_eval('ProductTask')
#task = Task()
#task = ProductTask()
#task.load_all()
#task.update_all()


#task = FinancialReportTask()
#task.run(date(2011,10,01), date(2011,12,31))
