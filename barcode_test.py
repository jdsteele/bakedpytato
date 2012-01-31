#!/usr/bin/python
import cfg
import re
from tasks import *
from models import BarcodeConversion, Manufacturer, ProductBarcode, Product, SupplierCatalogItem
from session import Session


session = Session(autocommit=True)

file_name = '/home/jdsteele/Desktop/bowser-inventory-20120130.txt'

#cache barcode_conversions
query = session.query(BarcodeConversion)
barcode_conversions = (query)

manufacturers = dict()
query = session.query(Manufacturer)
for manufacturer in query:
	manufacturers[manufacturer.id] = manufacturer


task = BarcodeConversionTask()

with open(file_name) as f:
	for line in f:
		line = line.rstrip()
		print line
		obj = task.get(line)
		if obj:
			print manufacturers[obj.manufacturer_id].identifier, '-', obj.identifier
