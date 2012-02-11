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


#cProfile.run( 'SupplierCatalogTask().load()' , '/tmp/fooprof')
#cProfile.run( 'SupplierSpecialTask().load_all()' , '/tmp/fooprof')


#task.update_all()

#task1 = SupplierCatalogItemVersionTask()
#cProfile.run( 'task1.load()' , 'fooprof')

#cProfile.run( 'SupplierCatalogItemVersionTask().vacuum()', '/tmp/fooprof' )


#cProfile.run( 'SupplierCatalogItemFieldTask().vacuum()', '/tmp/fooprof' )

cProfile.run( 'SupplierCatalogItemFieldTask().update_all()', '/tmp/fooprof' )

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

#from Crypto import Cipher, Random
#from Crypto.Util import RFC1751

#key = Random.get_random_bytes(128/8)

#ekey = RFC1751.key_to_english(key) 

#print ekey

#Krypt = Cipher.Blowfish

#c = Krypt.new(key, Krypt.MODE_CFB)

#e = c.encrypt('Hello World')
#print e


#key = RFC1751.english_to_key(ekey) 

#c = Krypt.new(key, Krypt.MODE_CFB)

#d = c.decrypt(e)
#print d
