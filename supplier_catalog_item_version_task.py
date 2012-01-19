#!/usr/bin/python
#from engine import enginemaker
#from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from sql_mapping import SupplierCatalog
from sql_mapping import SupplierCatalogItemVersion

import time

from caching_query import FromCache

from environment import Session
#from session import Session

from progressbar import Bar, Percentage, ETA, FileTransferSpeed, ProgressBar


session = Session(expire_on_commit=False)
session2 = Session()

query = session.query(SupplierCatalogItemVersion)

count = query.count()
i = 0;

pbar = ProgressBar(widgets=[Percentage(), ETA(), FileTransferSpeed(), Bar()], maxval=count).start()

print time.strftime('%Y-%m-%d %H:%M:%S %Z')

for supplier_catalog_item_version in query.yield_per(10000):
	
	#print i, '/', count, "\r",
	
	pbar.update(i)
	i+=1
	
	#session.begin()
	#session.add(supplier_catalog_item_version)
	
	#*** Supplier Catalog ***
	query2 = session2.query(SupplierCatalog).options(FromCache("default", "supplier_catalog"))
	query2 = query2.filter(SupplierCatalog.id == supplier_catalog_item_version.supplier_catalog_id)

	try:
		supplier_catalog = query2.one()
		supplier_catalog_item_version.next_supplier_catalog_id = supplier_catalog.next_supplier_catalog_id
	except NoResultFound:
		supplier_catalog_item_version.next_supplier_catalog_id = None
	#if supplier_catalog_item_version.is_dirty():
	if i % 100 == 0:
		session.flush()
		session2.flush()
	if i % 100000 == 0:
		print "\n", time.strftime('%Y-%m-%d %H:%M:%S %Z'), "\n"

print "\n", "Commiting", time.strftime('%Y-%m-%d %H:%M:%S %Z'), "\n"
session.commit()
print "\n", "Comitted", time.strftime('%Y-%m-%d %H:%M:%S %Z'), "\n"
