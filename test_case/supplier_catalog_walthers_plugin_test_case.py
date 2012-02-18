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
#Standard Library
import unittest
import datetime
import struct

from decimal import Decimal
from plugin.supplier_catalog_walthers_plugin import SupplierCatalogWalthersPlugin
from model import *

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


class SupplierCatalogWalthersPluginTestCase(unittest.TestCase):
	
	def setUp(self):
		self.maxDiff = None
		self.file_import = FileImportModel()
		self.supplier_catalog_filter = SupplierCatalogFilterModel()
		self.plugin = SupplierCatalogWalthersPlugin(self.supplier_catalog_filter)
		
	def test_match_file_import(self):
		self.file_import.name = "blargh"
		self.file_import.content = "blargh"
		
		result = self.plugin.match_file_import(self.file_import)
		self.assertFalse(result)

		self.file_import.name = "blarghwalthers/CatalogUpdate-12345678blargh"
		result = self.plugin.match_file_import(self.file_import)
		self.assertTrue(result)

	def test_get_items(self):
		self.file_import.content = ""
		supplier_catalog = SupplierCatalogModel()
		supplier_catalog.file_import = self.file_import
		for result in self.plugin.get_items(supplier_catalog):
			self.assertIsNone(result)

		c = [
			'19770901',
			'   1', '1         ', struct.pack('<LL', MASK_PRICE_RETAIL, 100),
			'   1', '2         ', struct.pack('<LL', MASK_PRICE_DEALER, 100),
			'   1', '3         ', struct.pack('<LL', MASK_AVAILABILITY, 19770901),
			'   1', '4         ', struct.pack('<Lc', MASK_IS_PHASED_OUT, 'Y'),
			'   1', '5         ', struct.pack('<Lc', MASK_IS_IN_STOCK, 'Y'),
			'   1', '6         ', struct.pack('<L', MASK_SCALE), 'H   ',
			'   1', '7         ', struct.pack('<L', MASK_CATEGORY), '1  ',
			'   1', '8         ', struct.pack('<L', MASK_NAME), "blargh\x00",
		]

		expected = [
			{'MANUFACTURER': '1', 'PRODUCT': '1', 'PRICE_RETAIL': 100},
			{'MANUFACTURER': '1', 'PRODUCT': '2', 'PRICE_DEALER': 100},
			{'MANUFACTURER': '1', 'PRODUCT': '3', 'AVAILABILITY': 19770901},
			{'MANUFACTURER': '1', 'PRODUCT': '4', 'IS_PHASED_OUT': 'Y'},
			{'MANUFACTURER': '1', 'PRODUCT': '5', 'IS_IN_STOCK': 'Y'},
			{'MANUFACTURER': '1', 'PRODUCT': '6', 'SCALE': 'H'},
			{'MANUFACTURER': '1', 'PRODUCT': '7', 'CATEGORY': '1'},
			{'MANUFACTURER': '1', 'PRODUCT': '8', 'NAME': 'blargh'},
		]

		self.file_import.content = str.join('', c)
		
		results = list(self.plugin.get_items(supplier_catalog))
		self.assertEqual(expected, results)

	def test_issue_date(self):
		self.file_import.content = "blarghblargh"
		self.file_import.effective = datetime.datetime(1976,7,4, 0, 0, 0)

		result = self.plugin.issue_date(self.file_import)
		self.assertEqual(result, self.file_import.effective)

		self.file_import.content = "19770901blargh"
		result = self.plugin.issue_date(self.file_import)
		self.assertEqual(result, datetime.datetime(1977, 9, 1, 0, 0, 0))

	def test_update_fields(self):
		fieldsets = [
			{'MANUFACTURER': '1', 'PRODUCT': '1', 'PRICE_RETAIL': 100},
			{'MANUFACTURER': '1', 'PRODUCT': '2', 'PRICE_DEALER': 100},
			{'MANUFACTURER': '1', 'PRODUCT': '3', 'AVAILABILITY': 19770901},
			{'MANUFACTURER': '1', 'PRODUCT': '4', 'IS_PHASED_OUT': 'Y'},
			{'MANUFACTURER': '1', 'PRODUCT': '5', 'IS_IN_STOCK': 'Y'},
			{'MANUFACTURER': '1', 'PRODUCT': '6', 'SCALE': 'H'},
			{'MANUFACTURER': '1', 'PRODUCT': '7', 'CATEGORY': '1'},
			{'MANUFACTURER': '1', 'PRODUCT': '8', 'NAME': 'blargh'},
			{'MANUFACTURER': '1', 'PRODUCT': '9', 'AVAILABILITY': 0},
			{'MANUFACTURER': '1', 'PRODUCT': '10', 'AVAILABILITY': 999999},
		]

		expected = [
			{'manufacturer_identifier': '1', 'product_identifier':'1', 'retail':Decimal(1)},
			{'manufacturer_identifier': '1', 'product_identifier':'2', 'cost':Decimal(1)},
			{'manufacturer_identifier': '1', 'product_identifier':'3', 'available': datetime.date(1977,9,1), 'availability_indefinite': False},
			{'manufacturer_identifier': '1', 'product_identifier':'4', 'phased_out':True},
			{'manufacturer_identifier': '1', 'product_identifier':'5', 'stock':True},
			{'manufacturer_identifier': '1', 'product_identifier':'6', 'scale_identifier':'H'},
			{'manufacturer_identifier': '1', 'product_identifier':'7', 'category_identifier':'1'},
			{'manufacturer_identifier': '1', 'product_identifier':'8', 'name':'blargh'},
			{'manufacturer_identifier': '1', 'product_identifier':'9', 'available': datetime.date(datetime.MINYEAR,1,1), 'availability_indefinite': False},
			{'manufacturer_identifier': '1', 'product_identifier':'10', 'available': datetime.date(datetime.MAXYEAR,1,1), 'availability_indefinite': True},
		]

		for i in xrange(len(fieldsets)):
			fieldset = fieldsets[i]
			expect = expected[i]

			result = self.plugin.update_fields(fieldset)
			self.assertEqual(result, expect)

