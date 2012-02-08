#!/usr/bin/python
# -*- coding: utf-8 -*-

#Standard Library
#from datetime import date

#Extended Library

#Application Library
import cfg
from task import *
import cProfile
import pstats



#from plugin import *
#from model import *

#task = SupplierCatalogTask()
#cProfile.run( 'task.load()' , 'fooprof')


#task.update_all()

#task1 = SupplierCatalogItemVersionTask()
#cProfile.run( 'task1.load()' , 'fooprof')

task2 = SupplierCatalogItemFieldTask()

task2.update_all()

#task1.update_all()

#task = SupplierCatalogItemTask()
#cProfile.run( 'task.update()' , 'fooprof')

#task = ProductTask()
#cProfile.run('task.load_all()', 'fooprof')
#cProfile.run('task.update_all()', 'fooprof')
#task.sort()

#task = CatalogItemTask()
#task.load_all()

#task = FinancialReportTask()
#task.run(date(2011,10,01), date(2011,12,31))

#task = SupplierCatalogItemFieldTask()
#task.update_all()

p = pstats.Stats('fooprof')
p.sort_stats('time').print_stats(40)
