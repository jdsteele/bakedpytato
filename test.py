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
from uuid import UUID

#from plugin import *
#from model import *
print "Testing..."

#cProfile.run( 'SupplierCatalogTask().load()' , '/tmp/fooprof')
#cProfile.run( 'SupplierCatalogTask().update()' , '/tmp/fooprof')
#cProfile.run( 'SupplierCatalogItemVersionTask().vacuum()', '/tmp/fooprof' )
#cProfile.run( 'SupplierCatalogItemVersionTask().load()' , '/tmp/fooprof')
#cProfile.run( 'SupplierCatalogItemVersionTask().update()' , '/tmp/fooprof')
#cProfile.run( 'SupplierCatalogItemFieldTask().vacuum()', '/tmp/fooprof' )
#cProfile.run( 'SupplierCatalogItemFieldTask().update()', '/tmp/fooprof' )
#cProfile.run( 'SupplierCatalogItemTask().load_all(supplier_id=UUID("4e8cfc8d-fa9c-4416-92e0-541066c1c7e4"), )' , '/tmp/fooprof')
cProfile.run( 'SupplierCatalogItemTask().load()' , '/tmp/fooprof')
#cProfile.run( 'SupplierCatalogItemTask().update()' , '/tmp/fooprof')

#cProfile.run( 'SupplierSpecialTask().load()' , '/tmp/fooprof')

#cProfile.run('ProductTask().load()', '/tmp/fooprof')
#cProfile.run('ProductTask().update()', '/tmp/fooprof')
#cProfile.run('ProductTask().sort()', '/tmp/fooprof')

#cProfile.run('CatalogItemTask().load()', '/tmp/fooprof')

#task = FinancialReportTask()
#task.run(date(2011,10,01), date(2011,12,31))


p = pstats.Stats('/tmp/fooprof')
p.sort_stats('time').print_stats(40)

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
