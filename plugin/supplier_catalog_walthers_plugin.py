# -*- coding: utf-8 -*-
"""
	BakedPotato — Inventory Management System

	BakedPotato IMS
	Copyright 2010-2012, John David Steele (john.david.steele@gmail.com)

	Licensed under The MIT License
	Redistributions of files must retain the above copyright notice.

	@copyright     Copyright 2010-2012, John David Steele (john.david.steele@gmail.com)
	@license       MIT License (http://www.opensource.org/licenses/mit-license.php)'cmp-
"""
#Standard Library
import logging 
import re
import struct
import tempfile
from datetime import date, datetime
from decimal import *

#Extended Library

#Application Library

#This Package
from plugin.base_supplier_catalog_plugin import BaseSupplierCatalogPlugin, Opaque

logger = logging.getLogger(__name__)


#Constants

MASK_PRICE_RETAIL = 0x1
MASK_PRICE_DEALER = 0x2
MASK_PRICE_BOX = 0x100000
MASK_PRICE_CASE = 0x200000
MASK_AVAILABILITY = 0x4
MASK_IS_PHASED_OUT = 0x8
MASK_IS_IN_STOCK = 0x10
MASK_IS_AVAILABLE = 0x100
MASK_SCALE = 0x40
MASK_DISCOUNT = 0x200
MASK_QTY_BOX = 0x400
MASK_QTY_CASE = 0x800
MASK_QTY_MINIMUM = 0x1000
MASK_CATEGORY = 0x2000
MASK_SUB_CATEGORY = 0x4000
MASK_CATALOG_PAGE = 0x8000
MASK_CATALOG = 0x10000
MASK_QTY_2 = 0x20000
MASK_QTY_4 = 0x40000
MASK_NAME = 0x80

AVAILABILITY_CODE = 999990
AVAILABILITY_UNKNOWN_6 = 999996
AVAILABILITY_UNKNOWN_7 = 999997
AVAILABILITY_SPECIAL_ORDER = 999998
AVAILABILITY_INDEFINITE = 999999

class SupplierCatalogWalthersPlugin(BaseSupplierCatalogPlugin):
	

	def match_file_import(self, file_import):
		if re.search('lock', file_import.name):
			return False
		if re.search(r'walthers/{1,2}CatalogUpdate[ -]\d{8}', file_import.name):
			return True
		return False

	def get_items(self, supplier_catalog):
		f = tempfile.SpooledTemporaryFile(max_size=(64*1024*1024))
		
		if supplier_catalog.file_import.content is None:
			return
		
		f.write(supplier_catalog.file_import.content)
		
		f_len = f.tell()
		
		f.seek(0)
		
		date = f.read(8)
		
		while f.tell() < f_len:
			data = dict()
			
			q = data['MANUFACTURER'] = f.read(4).strip(chr(0)).strip()
			
			if q == '':
				return
			
			data['PRODUCT'] = f.read(10).strip(chr(0)).strip()
			
			#print f.tell(), "OF", f_len
			
			mask = struct.unpack('<L', f.read(4))[0]
		
			if mask & MASK_PRICE_RETAIL:
				#Little Endian Unsigned Long
				data['PRICE_RETAIL'] = struct.unpack('<L', f.read(4))[0]
		
			if mask & MASK_PRICE_DEALER:
				#Little Endian Unsigned Long
				data['PRICE_DEALER'] = struct.unpack('<L', f.read(4))[0]
		
			if mask & MASK_PRICE_BOX:
				#Little Endian Unsigned Long
				data['PRICE_BOX'] = struct.unpack('<L', f.read(4))[0]
		
			if mask & MASK_PRICE_CASE:
				#Little Endian Unsigned Long
				data['PRICE_CASE'] = struct.unpack('<L', f.read(4))[0]
			
			if mask & MASK_AVAILABILITY:
				#Little Endian Unsigned Long
				data['AVAILABILITY'] = struct.unpack('<L', f.read(4))[0]

			if mask & MASK_IS_PHASED_OUT:
				#char
				data['IS_PHASED_OUT'] = f.read(1).strip(chr(0)).strip()

			if mask & MASK_IS_IN_STOCK:
				#char
				data['IS_IN_STOCK'] = f.read(1).strip(chr(0)).strip()

			if mask & MASK_IS_AVAILABLE:
				#char
				data['IS_AVAILABLE'] = f.read(1).strip(chr(0)).strip()
				
			if mask & MASK_SCALE:
				#char * 4
				data['SCALE'] = f.read(4).strip(chr(0)).strip()
				
			if mask & MASK_DISCOUNT:
				#char
				data['DISCOUNT'] = f.read(1).strip(chr(0)).strip()
				
			if mask & MASK_QTY_BOX:
				#Little Endian Unsigned Short
				data['QTY_BOX'] = struct.unpack('<H', f.read(2))[0]
				
			if mask & MASK_QTY_CASE:
				#Little Endian Unsigned Short
				data['QTY_CASE'] = struct.unpack('<H', f.read(2))[0]
				
			if mask & MASK_QTY_MINIMUM:
				#Little Endian Unsigned Short
				data['QTY_MINIMUM'] = struct.unpack('<H', f.read(2))[0]
				
			if mask & MASK_CATEGORY:
				#char * 3
				data['CATEGORY'] = f.read(3).strip(chr(0)).strip()
				
			if mask & MASK_SUB_CATEGORY:
				#char * 2
				data['SUB_CATEGORY'] = f.read(2).strip(chr(0)).strip()
				
			if mask & MASK_CATALOG_PAGE:
				#Little Endian Unsigned Short
				data['CATALOG_PAGE'] = struct.unpack('<H', f.read(2))[0]

			if mask & MASK_CATALOG:
				#char * 11
				data['CATALOG'] = f.read(11).strip(chr(0)).strip()

			if mask & MASK_QTY_2:
				#Little Endian Unsigned Short
				data['QTY_2'] = struct.unpack('<H', f.read(2))[0]

			if mask & MASK_QTY_4:
				#Little Endian Unsigned Short
				data['QTY_4'] = struct.unpack('<L', f.read(4))[0]

			if mask & MASK_NAME:
				#NULL Terminated String
				st = str()
				s = str()
				while (s != chr(0)):
					s = f.read(1)
					st = st + s
				data['NAME'] = st.strip(chr(0)).strip()
			yield data

	def issue_date(self, file_import):

		m = re.match('(\d{4})(\d{2})(\d{2})', file_import.content[:8])
		if m:
			return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))

		logger.warning("Failed to convert issue_date for %s", file_import.name)
		return file_import.effective


	def update_fields(self, fields):
		"""Update Fields"""
		
		data = dict()
		
		if 'MANUFACTURER' in fields and fields['MANUFACTURER'] is not None:
			data['manufacturer_identifier'] = fields['MANUFACTURER']
			
		if 'PRODUCT' in fields and fields['PRODUCT'] is not None:
			data['product_identifier'] = fields['PRODUCT']

		if 'SCALE' in fields and fields['SCALE'] is not None:
			data['scale_identifier'] = fields['SCALE']
			
		if 'CATEGORY' in fields and fields['CATEGORY'] is not None:
			data['category_identifier'] = fields['CATEGORY']

		if 'NAME' in fields and fields['NAME'] is not None:
			data['name'] = fields['NAME']
			
		if 'PRICE_RETAIL' in fields and fields['PRICE_RETAIL'] is not None:
			data['retail'] = Decimal(fields['PRICE_RETAIL']) / Decimal(100)

		if 'PRICE_DEALER' in fields and fields['PRICE_DEALER'] is not None:
			data['cost'] = Decimal(fields['PRICE_DEALER']) / Decimal(100)
			
		if 'AVAILABILITY' in fields and fields['AVAILABILITY'] is not None:
			if fields['AVAILABILITY'] < 1000000 and fields['AVAILABILITY'] > 0:
				data['availability_indefinite'] = True
				data['available'] = Opaque
			elif fields['AVAILABILITY'] == 0:
				data['availability_indefinite'] = False
				data['available'] = Opaque
			else:
				m = re.match(r'^(\d{4})(\d{2})(\d{2})$', str(fields['AVAILABILITY']))
				if m:
					data['availability_indefinite'] = False
					data['available'] = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
				else:
					logger.error("Field AVAILABILITY has unexpected value %s", fields['AVAILABILITY'])
					
		if 'IS_PHASED_OUT' in fields and fields['IS_PHASED_OUT'] is not None:
			if fields['IS_PHASED_OUT'] in ['Y', 'N']:
				data['phased_out'] = (fields['IS_PHASED_OUT'] == 'Y')
			else:
				logger.error("Field IS_PHASED_OUT has unexpected value %s", fields['IS_PHASED_OUT'])

		if 'IS_IN_STOCK' in fields and fields['IS_IN_STOCK'] is not None:
			if fields['IS_IN_STOCK'] in ['Y', 'N']:
				data['stock'] = (fields['IS_IN_STOCK'] == 'Y')
			else:
				logger.error("Field IS_IN_STOCK has unexpected value %s", fields['IS_IN_STOCK'])
		#print fields
		#print data
		return data

