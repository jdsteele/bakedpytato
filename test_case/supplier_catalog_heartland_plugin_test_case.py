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
from plugin.supplier_catalog_heartland_plugin import SupplierCatalogHeartlandPlugin
from model import *

class SupplierCatalogHeartlandPluginTestCase(unittest.TestCase):
	
	def setUp(self):
		self.maxDiff = None
		self.file_import = FileImportModel()
		self.supplier_catalog_filter = SupplierCatalogFilterModel()
		self.plugin = SupplierCatalogHeartlandPlugin(self.supplier_catalog_filter)
		
	def ztest_match_file_import(self):
		self.file_import.name = "blargh"
		self.file_import.content = "blargh"
		
		result = self.plugin.match_file_import(self.file_import)
		self.assertFalse(result)

		self.file_import.name = "blarghemeryblargh"
		result = self.plugin.match_file_import(self.file_import)
		self.assertTrue(result)

	def test_get_items(self):
		self.file_import.content = ""
		supplier_catalog = SupplierCatalogModel()
		supplier_catalog.file_import = self.file_import
		for result in self.plugin.get_items(supplier_catalog):
			self.assertIsNone(result)

		c = [
			'"AAC41821C      ","SCULPTAMOLD 3LB. BAG     ",7.49     ',
			'"KAD11          ","# HO NO 5 BULK PACK 20PR ",27.95    ',
			'"KAD804         ","O COUPLER/GEAR BOX, PLAST",4.20     ',
			''
		]
		self.file_import.content = "\n".join(c)
		
		expected = [
			{
				'Name': 'SCULPTAMOLD 3LB. BAG', 
				'SKU': 'AAC41821C', 
				'Retail': '7.49', 
			},
			{
				'Name': '# HO NO 5 BULK PACK 20PR', 
				'SKU': 'KAD11', 
				'Retail': '27.95', 
			},
			{
				'Name': 'O COUPLER/GEAR BOX, PLAST', 
				'Retail': '4.20', 
				'SKU': 'KAD804'
			},
			None
		]
		
		results = list(self.plugin.get_items(supplier_catalog))
		self.assertEqual(expected, results)

	def ztest_issue_date(self):
		self.file_import.name = "blarghblargh"
		self.file_import.effective = datetime.datetime(1976,7,4, 0, 0, 0)

		result = self.plugin.issue_date(self.file_import)
		self.assertEqual(result, self.file_import.effective)

		self.file_import.name = "19770901.CSV"
		result = self.plugin.issue_date(self.file_import)
		self.assertEqual(result, datetime.datetime(1977, 9, 1, 0, 0, 0))

	def test_update_fields(self):
		fieldsets = [
			{
				'Name': 'SCULPTAMOLD 3LB. BAG', 
				'SKU': 'AAC41821C', 
				'Retail': '7.49', 
			},
			{
				'Name': '# HO NO 5 BULK PACK 20PR', 
				'SKU': 'KAD11', 
				'Retail': '27.95', 
			},
			{
				'Name': 'O COUPLER/GEAR BOX, PLAST', 
				'Retail': '4.20', 
				'SKU': 'KAD804'
			},
			None
		]

		expected = [
			{
				'cost': Decimal('7.49') * (Decimal('100') - Decimal('44.3')) / Decimal('100'),
				'manufacturer_identifier': 'AAC',
				'name': 'SCULPTAMOLD 3LB. BAG',
				'product_identifier': '41821C',
				'retail': Decimal('7.49'),
				'stock': True,
				'scale': None
			},
			{
				'cost': Decimal('27.95') * (Decimal('100') - Decimal('25')) / Decimal('100'),
				'manufacturer_identifier': 'KAD',
				'name': '# HO NO 5 BULK PACK 20PR',
				'product_identifier': '11',
				'retail': Decimal('27.95'),
				'scale': 'HO',
				'stock': True
			},
			{
				'scale': 'O', 
				'cost': Decimal('4.20') * (Decimal('100') - Decimal('44.3')) / Decimal('100'),
				'name': 'O COUPLER/GEAR BOX, PLAST', 
				'manufacturer_identifier': 'KAD', 
				'product_identifier': '804', 
				'retail': Decimal('4.20'), 
				'stock': True
			},
			None
		]

		for i in xrange(len(fieldsets)):
			fieldset = fieldsets[i]
			expect = expected[i]

			result = self.plugin.update_fields(fieldset)
			self.assertEqual(result, expect)

