#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	BakedPotato — Inventory Management System

	BakedPotato IMS
	Copyright 2010-2012, John David Steele (john.david.steele@gmail.com)

	Licensed under The MIT License
	Redistributions of files must retain the above copyright notice.

	@copyright     Copyright 2010-2012, John David Steele (john.david.steele@gmail.com)
	@license       MIT License (http://www.opensource.org/licenses/mit-license.php)
"""

#Pragma
from __future__ import unicode_literals

#Standard Library
#import logging 
import uuid
import tempfile
#from decimal import *
import time

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

local_engine = session.local_engine()
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
	ts.add(ttystatus.Integer('done'))
	ts.add(ttystatus.Literal(' of '))
	ts.add(ttystatus.Integer('total'))
	ts['total'] = total
	ts['done'] = 0
	return ts

def uuid_to_int(i):
	u = uuid.UUID(i)
	return u.int

def int_to_uuid(i):
	u = uuid.UUID(int=i)
	return str(u)

def get_lines(f, line_count):
	lines = []
	i = 0
	while True:
		line = f.readline().rstrip()
		if line == "" or line is None:
			if len(lines) > 0:
				yield lines
			break
		if i == line_count:
			yield lines
			lines = []
			i = 0
		lines.append(line)
		i += 1

def delete(deletable_f):
	#Delete
	deletable_len = deletable_f.tell()
	deletable_f.seek(0)

	ts = get_ts(deletable_len, 'Deleting')
	#deletable_id = deletable_f.readline().rstrip()
	#while (deletable_id is not None) and (deletable_id != ''):
	for lines in get_lines(deletable_f, 200):
		local_engine.begin()
		remote_engine.begin()
		s = remote_table.delete().where(local_table.c.id.in_(lines))
		#s = local_table.delete().where(local_table.c.id == deletable_id)
		result = local_engine.execute(s)
		ts['done'] = deletable_f.tell()
		#deletable_id = deletable_f.readline().rstrip()
		remote_engine.commit()
		local_engine.commit()
	deletable_f.close()
	ts.finish()

def insert(insertable_f):
	#Insert
	insertable_len = insertable_f.tell()
	insertable_f.seek(0)

	ts = get_ts(insertable_len, 'Inserting')
	for lines in get_lines(insertable_f, 10):
		local_engine.begin()
		remote_engine.begin()
		s = remote_table.select().where(remote_table.c.id.in_(lines))
		#print s
		remote_results = remote_engine.execute(s)
		#print remote_results
		rows = remote_results.fetchall()
		for row in rows:
			d = dict()
			for (key, val) in row.items():
				d[key] = val
			ss = local_table.insert().values(d)
			local_result = local_engine.execute(ss)
		ts['done'] = insertable_f.tell()
		remote_engine.commit()
		local_engine.commit()
		time.sleep(0.01)
	insertable_f.close()
	ts.finish()

def update(updatable_f):
	#Update

	updatable_len = updatable_f.tell()
	if updatable_len is None:
		return
	updatable_f.seek(0)
	ts = get_ts(updatable_len, 'Updating')
	for lines in get_lines(updatable_f, 10):
		local_engine.begin()
		remote_engine.begin()
		s = remote_table.select().where(remote_table.c.id.in_(lines))
		#print s
		remote_results = remote_engine.execute(s)
		#print remote_results
		rows = remote_results.fetchall()
		for row in rows:
			#print row.items()
			d = dict()
			for (key, val) in row.items():
				d[key] = val
			ss = local_table.update().values(d).where(local_table.c.id == d['id'])
			#print ss
			local_result = local_engine.execute(ss)
			
		remote_engine.commit()
		local_engine.commit()
		time.sleep(0.01)
		ts['done'] = updatable_f.tell()
	updatable_f.close()
	ts.finish()



table_names = [
	#['barcode_conversions', 'ALL'],
	#['catalog_items', 'ALL'],
	['category_conversions', 'ALL'],
	#['customer_incidentals', 'ALL'],
	#['customer_order_items', 'ALL'],
	#['customer_orders', 'ALL'],
	#['customer_shipment_items', 'ALL'],
	['file_imports', 'ALL'],
	#['inventory_items', 'ALL'],
	['manufacturer_conversions', 'ALL'],
	['manufacturers', 'ALL'],
	['price_controls', 'ALL'],
	#['product_barcodes', 'ALL'],
	['product_conversions', 'ALL'],
	#['products', 'ALL'],
	['scale_conversions', 'ALL'],
	['scales', 'ALL'],
	['supplier_catalog_filters', 'ALL'],
	#['supplier_catalog_items', 'ALL'],
	#['supplier_catalog_item_fields', 'ALL'],
	#['supplier_catalog_item_bowser_versions', 'ALL'],
	#['supplier_catalog_item_emery_versions', 'ALL'],
	#['supplier_catalog_item_exactrail_versions', 'ALL'],
	#['supplier_catalog_item_walthers_versions', 'ALL'],
	#['supplier_catalogs', 'ALL'],
	['suppliers', 'ALL']
]


table_count = len(table_names)
table_i = 0
for (table_name, operations) in table_names:
	table_i += 1
	print table_name, table_i, '/', table_count
	local_table = Table(table_name, local_meta, autoload=True)
	remote_table = Table(table_name, remote_meta, autoload=True)

	remote_f = tempfile.SpooledTemporaryFile(max_size=(256*1024*1024))
	local_f = tempfile.SpooledTemporaryFile(max_size=(256*1024*1024))

	print 'Getting Remote Ids...'
	remote_engine.begin()
	s = select([remote_table.c.id]).order_by(remote_table.c.id.asc())
	result = remote_engine.execute(s)
	for r in result:
		remote_f.write(r.id + "\n")
	del result
	
	remote_len = remote_f.tell()
	
	remote_f.seek(0)
	remote_engine.commit()

	print 'Getting Local Ids...'
	local_engine.begin()
	s = select([local_table.c.id]).order_by(local_table.c.id.asc())
	result = local_engine.execute(s)
	for r in result:
		local_f.write(r.id + "\n")
	del result

	local_len = local_f.tell()

	local_f.seek(0)
	local_engine.commit()
	
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
				#print "Both files have reached EOF. break out of loop"
				break
			else:
				print "remote file has reached EOF"
				#all remaining ids in local file are deletable
				deletable_f.write(local_id + "\n")
				local_id = local_f.readline().rstrip()
				continue

		if (local_id == '') or (local_id is None):
			#print "local file has reached EOF"
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

	if operations == 'ALL' or 'ALL' in operations:
		delete(deletable_f)
		insert(insertable_f)
		update(updatable_f)
		
	if 'DELETE' in operations:
		delete(deletable_f)
		
	if 'INSERT' in operations:
		insert(insertable_f)
		
	if 'UPDATE' in operations:
		update(uptatable_f)
