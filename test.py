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

#cProfile.run( 'SupplierCatalogItemFieldTask().update_all()', '/tmp/fooprof' )

#task2.update_all()

#task1.update_all()

#cProfile.run( 'SupplierCatalogItemTask().load()' , '/tmp/fooprof')

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

#p = pstats.Stats('/tmp/fooprof')
#p.sort_stats('time').print_stats(40)

import math
from decimal import *

tax_rate = Decimal(0.06)
old_tax = 0
for x in xrange(1,1001):
	total = Decimal(x)
	low = int(total * tax_rate * 99)
	high = low + 2
	#print total, low, high
	done = False
	for t in xrange(low,high):
		tax = Decimal(t) / Decimal(100)
		principal = total - tax
		if principal * tax_rate <= tax:
			print ('%6.2f = P(%6.2f) + T(%6.2f)' % (total, principal, tax))
			done = True
			break
	if done is False:
		exit(0)
	
