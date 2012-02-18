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
from decimal import Decimal
from plugin.supplier_catalog_bowser_plugin import SupplierCatalogBowserPlugin
from model import *

class SupplierCatalogBowserPluginTestCase(unittest.TestCase):
	
	def setUp(self):
		
		self.file_import = FileImportModel()
		self.supplier_catalog_filter = SupplierCatalogFilterModel()
		self.plugin = SupplierCatalogBowserPlugin(self.supplier_catalog_filter)
		
	def test_match_file_import(self):
		self.file_import.name = "blargh"
		self.file_import.content = "blargh"
		
		result = self.plugin.match_file_import(self.file_import)
		self.assertFalse(result)

		self.file_import.name = "blarghDealerOutsideWebExportblargh"
		result = self.plugin.match_file_import(self.file_import)
		self.assertFalse(result)

		self.file_import.content = "blarghBowserblargh"
		result = self.plugin.match_file_import(self.file_import)
		self.assertTrue(result)


	def test_get_items(self):
		self.file_import.content = ""
		supplier_catalog = SupplierCatalogModel()
		supplier_catalog.file_import = self.file_import
		for result in self.plugin.get_items(supplier_catalog):
			self.assertIsNone(result)

		self.file_import.content = (
			"manufacturer	item	description1	price1	category--1	category--2	category--3	stock	description2	retail	discount\n"+
			"1	2	Bowser Widget 2	9.99	category--1	category--2	category--3	50	description2	$18.99	40\n"+
			"1	3	Bowser Widget 3	9.99	category--1	category--2	category--3	0	description2	$18.99	40\n"
			"1	4	Bowser Widget 4	9.99	category--1	category--2	category--3	-10000	description2	$18.99	40\n"
			"1	5	Bowser Widget 5 Due 7/4/1976	9.99	category--1	category--2	category--3	-10000	7/4/1976	$18.99	40\n"
		)
		
		expected = [
			{'Category1': 'category--1', 'Category3': 'category--3', 'Category2': 'category--2', 'Retail': 'retail', 'Discount': 'discount', 'Item': 'item', 'Description2': 'description2', 'Description1': 'description1', 'Price1': 'price1', 'Stock': 'stock', 'Manufacturer': 'manufacturer'},
			{'Category1': 'category--1', 'Category3': 'category--3', 'Category2': 'category--2', 'Retail': '$18.99', 'Discount': '40', 'Item': '2', 'Description2': 'description2', 'Description1': 'Bowser Widget 2', 'Price1': '9.99', 'Stock': '50', 'Manufacturer': '1'},
			{'Category1': 'category--1', 'Category3': 'category--3', 'Category2': 'category--2', 'Retail': '$18.99', 'Discount': '40', 'Item': '3', 'Description2': 'description2', 'Description1': 'Bowser Widget 3', 'Price1': '9.99', 'Stock': '0', 'Manufacturer': '1'},
			{'Category1': 'category--1', 'Category3': 'category--3', 'Category2': 'category--2', 'Retail': '$18.99', 'Discount': '40', 'Item': '4', 'Description2': 'description2', 'Description1': 'Bowser Widget 4', 'Price1': '9.99', 'Stock': '-10000', 'Manufacturer': '1'},
			{'Category1': 'category--1', 'Category3': 'category--3', 'Category2': 'category--2', 'Retail': '$18.99', 'Discount': '40', 'Item': '5', 'Description2': '7/4/1976', 'Description1': 'Bowser Widget 5 Due 7/4/1976', 'Price1': '9.99', 'Stock': '-10000', 'Manufacturer': '1'},
			None
		]
		
		results = list(self.plugin.get_items(supplier_catalog))
		self.assertEqual(expected, results)

	def test_issue_date(self):
		self.file_import.name = "blarghDealerOutsideWebExportblargh"
		self.file_import.effective = datetime.datetime(1976,7,4, 0, 0, 0)

		result = self.plugin.issue_date(self.file_import)
		self.assertEqual(result, self.file_import.effective)

		self.file_import.name = "9-1-1977 DealerOutsideWebExport"
		result = self.plugin.issue_date(self.file_import)
		self.assertEqual(result, datetime.datetime(1977, 9, 1, 0, 0, 0))

		self.file_import.name = "8-1-1977 Bowser DealerOutsideWebExport"
		result = self.plugin.issue_date(self.file_import)
		self.assertEqual(result, datetime.datetime(1977, 8, 1, 0, 0, 0))

	def test_update_fields(self):
		
		fieldsets = [
			{'Category1': 'category--1', 'Category3': 'category--3', 'Category2': 'category--2', 'Retail': '$18.99', 'Discount': '40', 'Item': '2', 'Description2': 'description2', 'Description1': 'Bowser Widget 2', 'Price1': '9.99', 'Stock': '50', 'Manufacturer': '1'},
			{'Category1': 'category--1', 'Category3': 'category--3', 'Category2': 'category--2', 'Retail': '$18.99', 'Discount': '40', 'Item': '3', 'Description2': 'description2', 'Description1': 'Bowser Widget 3', 'Price1': '9.99', 'Stock': '0', 'Manufacturer': '1'},
			{'Category1': 'category--1', 'Category3': 'category--3', 'Category2': 'category--2', 'Retail': '$18.99', 'Discount': '40', 'Item': '4', 'Description2': 'description2', 'Description1': 'Bowser Widget 4', 'Price1': '9.99', 'Stock': '-10000', 'Manufacturer': '1'},
			{'Category1': 'category--1', 'Category3': 'category--3', 'Category2': 'category--2', 'Retail': '$18.99', 'Discount': '40', 'Item': '5', 'Description2': '7/4/1976', 'Description1': 'Bowser Widget 5 Due 7/4/1976', 'Price1': '9.99', 'Stock': '-10000', 'Manufacturer': '1'},
			None
		]
		expected = [
			{	'advanced': False,
				'availability_indefinite': None,
				'available': None,
				'category_identifier': 'category--1',
				'cost': Decimal('11.394'),
				'manufacturer_identifier': '1',
				'name': 'Widget 2',
				'phased_out': False,
				'product_identifier': '2',
				'retail': Decimal('18.99'),
				'special_cost': Decimal('0'),
				'stock': True
			},
			{
				'advanced': False,
				'availability_indefinite': None,
				'available': None,
				'category_identifier': 'category--1',
				'cost': Decimal('11.394'),
				'manufacturer_identifier': '1',
				'name': 'Widget 3',
				'phased_out': False,
				'product_identifier': '3',
				'retail': Decimal('18.99'),
				'special_cost': Decimal('0'),
				'stock': False
			},
			{
				'advanced': True,
				'availability_indefinite': True,
				'available': datetime.date(datetime.MAXYEAR, 1, 1),
				'category_identifier': 'category--1',
				'cost': Decimal('11.394'),
				'manufacturer_identifier': '1',
				'name': 'Widget 4',
				'phased_out': False,
				'product_identifier': '4',
				'retail': Decimal('18.99'),
				'special_cost': Decimal('0'),
				'stock': False
			},
			{
				'advanced': True,
				'availability_indefinite': False,
				'available': datetime.date(1976, 7, 4),
				'category_identifier': 'category--1',
				'cost': Decimal('11.394'),
				'manufacturer_identifier': '1',
				'name': 'Widget 5 Due 7/4/1976',
				'phased_out': False,
				'product_identifier': '5',
				'retail': Decimal('18.99'),
				'special_cost': Decimal('0'),
				'stock': False
			},
			None
		]

		for i in xrange(len(fieldsets)):
			fieldset = fieldsets[i]
			expect = expected[i]

			result = self.plugin.update_fields(fieldset)
			self.assertEqual(result, expect)

