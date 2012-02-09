#!/usr/bin/python2.7
#Standard Library
#import logging 
import uuid
import tempfile
#from decimal import *

#Extended Library
#from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import *
from sqlalchemy.sql import *
import ttystatus

#Application Library
#from models import CustomerOrderItem, CustomerShipmentItem
#from models import InventoryItem
#from models import Product
#from models import SupplierCatalogItem
#from priceutil import decimal_psych_price
#import cfg
import session

#This Package
#from tasks.base_task import BaseTask
#from tasks.supplier_catalog_item_task import SupplierCatalogItemTask

local_engine = session.engine
remote_engine = session.remote_engine()

local_meta = MetaData()
local_meta.bind = local_engine
remote_meta = MetaData()
remote_meta.bind = remote_engine


def get_ts(total, text):
	ts = ttystatus.TerminalStatus(period=0.5)
	ts.add(ttystatus.Literal(text + ' '))
	ts.add(ttystatus.Literal(' Elapsed: '))
	ts.add(ttystatus.ElapsedTime())
	ts.add(ttystatus.Literal(' Remaining: '))
	ts.add(ttystatus.RemainingTime('done', 'total'))
	ts.add(ttystatus.Literal(' '))
	ts.add(ttystatus.PercentDone('done', 'total', decimals=2))
	ts.add(ttystatus.Literal(' '))
	ts.add(ttystatus.ProgressBar('done', 'total'))
	ts['total'] = total
	ts['done'] = 0
	return ts

def uuid_to_int(i):
	u = uuid.UUID(i)
	return u.int

def int_to_uuid(i):
	u = uuid.UUID(int=i)
	return str(u)

table_names = [
	#'barcode_conversions',
	#'catalog_items',
	#'category_conversions',
	#'customer_incidentals',
	#'customer_order_items',
	#'customer_orders',
	#'customer_shipment_items',
	'file_imports', 
	#'inventory_items',
	#'manufacturer_conversions',
	#'manufacturers',
	#'price_controls',
	#'product_barcodes',
	#'product_conversions',
	#'products',
	#'scale_conversions',
	#'scales',
	'supplier_catalog_filters',
	'supplier_catalog_items', 
	#'supplier_catalog_item_fields', 
	#'supplier_catalog_item_versions',
	'supplier_catalogs'
]


table_count = len(table_names)
table_i = 0
for table_name in table_names:
	table_i += 1
	print table_name, table_i, '/', table_count
	local_table = Table(table_name, local_meta, autoload=True)
	remote_table = Table(table_name, remote_meta, autoload=True)

	remote_f = tempfile.SpooledTemporaryFile(max_size=(256*1024*1024))
	local_f = tempfile.SpooledTemporaryFile(max_size=(256*1024*1024))

	print 'Getting Remote Ids...'

	s = select([remote_table.c.id]).order_by(remote_table.c.id.asc())
	result = remote_engine.execute(s)
	for r in result:
		remote_f.write(r.id + "\n")
	del result
	
	remote_len = remote_f.tell()
	
	remote_f.seek(0)

	print 'Getting Local Ids...'

	s = select([local_table.c.id]).order_by(local_table.c.id.asc())
	result = local_engine.execute(s)
	for r in result:
		local_f.write(r.id + "\n")
	del result

	local_len = local_f.tell()

	local_f.seek(0)

	updatable_f = tempfile.SpooledTemporaryFile(max_size=(256*1024*1024))
	insertable_f = tempfile.SpooledTemporaryFile(max_size=(256*1024*1024))
	deletable_f = tempfile.SpooledTemporaryFile(max_size=(256*1024*1024))

	remote_id = remote_f.readline().rstrip()
	local_id = local_f.readline().rstrip()

	l = local_len + remote_len

	ts = get_ts(l, 'Generating Sets')

	while True:
		ts['done'] = local_f.tell() + remote_f.tell()
		
		if (remote_id == '') or (remote_id is None):
			if (local_id == '') or (local_id is None):
				# Both files have reached EOF. break out of loop
				break
			else:
				#remote file has reached EOF
				#all remaining ids in local file are deletable
				deletable_f.write(local_id + "\n")
				local_id = local_f.readline().rstrip()
				continue

		if (local_id == '') or (local_id is None):
			#local file has reached EOF
			#all remaining ids in remote file are insertable
			insertable_f.write(remote_id + "\n")
			remote_id = remote_f.readline().rstrip()
			continue
		
		if remote_id == local_id:
			#print remote_id, '=', local_id
			#id exists in both files, is updatable
			updatable_f.write(local_id + "\n")
			remote_id = remote_f.readline().rstrip()
			local_id = local_f.readline().rstrip()
			continue

		if remote_id > local_id:
			#print remote_id, '>', local_id
			#local_id is not in remote file, is deletable
			deletable_f.write(local_id + "\n")
			local_id = local_f.readline().rstrip()
			continue

		if remote_id < local_id:
			#print remote_id, '<', local_id
			#remote_id is not in local file, is insertable
			insertable_f.write(remote_id + "\n")
			remote_id = remote_f.readline().rstrip()

	remote_f.close()
	local_f.close()
	ts.finish()
	
	#Delete
	
	deletable_len = deletable_f.tell()
	deletable_f.seek(0)

	ts = get_ts(deletable_len, 'Deleting')
	deletable_id = deletable_f.readline().rstrip()
	while (deletable_id is not None) and (deletable_id != ''):
		s = local_table.delete().where(local_table.c.id == deletable_id)
		result = local_engine.execute(s)
		ts['done'] = deletable_f.tell()
		deletable_id = deletable_f.readline().rstrip()
	ts.finish()
	deletable_f.close()

	#Insert

	insertable_len = insertable_f.tell()
	insertable_f.seek(0)

	ts = get_ts(insertable_len, 'Inserting')
	insertable_id = insertable_f.readline().rstrip()
	while (insertable_id is not None) and (insertable_id != ''):
		s = remote_table.select().where(remote_table.c.id == insertable_id)
		##print s
		remote_results = remote_engine.execute(s)

		row = remote_results.fetchone()

		##print remote_result
		d = dict()
		for (key, val) in row.items():
			d[key] = val

		s = local_table.insert().values(d)
		##print s
		local_result = local_engine.execute(s)
		ts['done'] = insertable_f.tell()
		insertable_id = insertable_f.readline().rstrip()
	ts.finish()
	insertable_f.close()
	
	#Update
	
	updatable_len = updatable_f.tell()
	updatable_f.seek(0)

	ts = get_ts(updatable_len, 'Updating')
	updatable_id = updatable_f.readline().rstrip()
	while (updatable_id is not None) and (updatable_id != ''):
		s = remote_table.select().where(remote_table.c.id == updatable_id)
		##print s
		remote_results = remote_engine.execute(s)

		row = remote_results.fetchone()

		##print remote_result
		d = dict()
		for (key, val) in row.items():
			d[key] = val

		s = local_table.update().values(d).where(local_table.c.id == updatable_id)
		##print s
		local_result = local_engine.execute(s)
		ts['done'] = updatable_f.tell()
		updatable_id = updatable_f.readline().rstrip()
	ts.finish()
	updatable_f.close()
