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
from plugin.supplier_special_walthers_plugin import SupplierSpecialWalthersPlugin
from model import *

class SupplierSpecialWalthersPluginTestCase(unittest.TestCase):
	
	def setUp(self):
		self.maxDiff = None
		self.file_import = FileImportModel()
		self.supplier_special_filter = SupplierSpecialFilterModel()
		self.plugin = SupplierSpecialWalthersPlugin(self.supplier_special_filter)
		
	def ztest_match_file_import(self):
		self.file_import.name = "blargh"
		self.file_import.content = "blargh"
		
		result = self.plugin.match_file_import(self.file_import)
		self.assertFalse(result)

		self.file_import.name = "blarghwalthers/CatalogUpdate-12345678blargh"
		result = self.plugin.match_file_import(self.file_import)
		self.assertTrue(result)

	def test_get_items(self):
		self.file_import.content = ""
		supplier_special = SupplierSpecialModel()
		supplier_special.file_import = self.file_import
		for result in self.plugin.get_items(supplier_special):
			self.assertIsNone(result)
			
		c = [
			'2/3/12 Hotlist',
			'MANU-ITEM #  ITEM DESCRIPTION       SCALE  RET $   Dlr Net  Dlr %',
			'433-1376       Snap-Loc elvtd pass stn       H    17.98   5.39   70%  ',
			'433-1992       Pruned Trees 2.5" 4/          H    8.99    2.00   78%  ',
			'6-55952       F-30 Flat Car CR MOW grey H       13.95    4.88   65%', #from 20100301
			''
		]
		
		expected = [
			{
				'MANU-ITEM':'433-1376', 
				'DESCRIPTION':'Snap-Loc elvtd pass stn', 
				'SCALE':'H', 
				'RET':'17.98',
				'DLR':'5.39',
				'DISC':'70%'
			},
			{
				'MANU-ITEM':'433-1992', 
				'DESCRIPTION':'Pruned Trees 2.5" 4/', 
				'SCALE':'H',
				'RET':'8.99', 
				'DLR':'2.00',
				'DISC':'78%'
			},
			{
				'MANU-ITEM':'6-55952', 
				'DESCRIPTION':'F-30 Flat Car CR MOW grey', 
				'SCALE':'H',
				'RET':'13.95', 
				'DLR':'4.88',
				'DISC':'65%'
			},
			None
		]

		self.file_import.content = str.join("\n", c)
		
		results = list(self.plugin.get_items(supplier_special))
		self.assertEqual(expected, results)



	def ztest_issue_date(self):
		self.file_import.content = "blarghblargh"
		self.file_import.effective = datetime.datetime(1976,7,4, 0, 0, 0)

		result = self.plugin.issue_date(self.file_import)
		self.assertEqual(result, self.file_import.effective)

		self.file_import.content = "19770901blargh"
		result = self.plugin.issue_date(self.file_import)
		self.assertEqual(result, datetime.datetime(1977, 9, 1, 0, 0, 0))

	def ztest_update_fields(self):
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

