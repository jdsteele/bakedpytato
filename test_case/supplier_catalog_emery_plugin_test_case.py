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
import cfg
from decimal import Decimal
from plugin.supplier_catalog_emery_plugin import SupplierCatalogEmeryPlugin
from model import *

class SupplierCatalogEmeryPluginTestCase(unittest.TestCase):
	
	def setUp(self):
		self.maxDiff = None
		self.file_import = FileImportModel()
		self.supplier_catalog_filter = SupplierCatalogFilterModel()
		self.plugin = SupplierCatalogEmeryPlugin(self.supplier_catalog_filter)
		
	def test_match_file_import(self):
		self.file_import.name = "blargh"
		self.file_import.content = "blargh"
		
		result = self.plugin.match_file_import(self.file_import)
		self.assertFalse(result)

		self.file_import.name = "blarghemeryblargh"
		result = self.plugin.match_file_import(self.file_import)
		self.assertTrue(result)

		self.file_import.name = cfg.emery_user + "xp-20100101.CSV"
		result = self.plugin.match_file_import(self.file_import)
		self.assertTrue(result)

	def test_get_items(self):
		self.file_import.content = ""
		supplier_catalog = SupplierCatalogModel()
		supplier_catalog.file_import = self.file_import
		for result in self.plugin.get_items(supplier_catalog):
			self.assertIsNone(result)

		c = [
			'VPARTNO	DESCRIP	SCALE	CATEGORY	PRICE	COST	INSTOCK	ENDOFLIFE	ONSALE	DITEM	_NullFlags',
			'"AFX1012"	"Track Clip/10pk"	""	"Toy Slot Cars"	        9.50000	        5.13000	""	""	"No"	"http://www.emerydistributors.com/Images/ProductImages/1071012.jpg"',
			'"ATL20000357"	"HO 89\'Flat Erie Western #250051"	"1/87"	"Toy Trains HO Scale"	       35.95000	       14.38000	"YES"	""	"Yes"	"http://www.emerydistributors.com/Images/ProductImages/15020000357.jpg"',
			'"ATL20000426"	"HO 25,500g Tank Car PLMX #25133"	"1/87"	"Toy Trains HO Scale"	       29.95000	       16.18000	""	"DISC"	"No"	"http://www.emerydistributors.com/Images/ProductImages/15020000426.jpg"',
			''
		]
		self.file_import.content = "\n".join(c)
		
		expected = [
			{
				'CATEGORY': 'Toy Slot Cars', 
				'ONSALE': 'No', 
				'SCALE': None, 
				'ENDOFLIFE': None, 
				'PRICE': '9.50000', 
				'COST': '5.13000', 
				'DITEM': 'http://www.emerydistributors.com/Images/ProductImages/1071012.jpg', 
				'INSTOCK': None, 
				'DESCRIP': 'Track Clip/10pk', 
				'VPARTNO': 'AFX1012'
			},
			{
				'CATEGORY': 'Toy Trains HO Scale', 
				'ONSALE': 'Yes', 
				'SCALE': '1/87', 
				'ENDOFLIFE': None, 
				'PRICE': '35.95000', 
				'COST': '14.38000', 
				'DITEM': 'http://www.emerydistributors.com/Images/ProductImages/15020000357.jpg', 
				'INSTOCK': 'YES', 
				'DESCRIP': "HO 89'Flat Erie Western #250051", 
				'VPARTNO': 'ATL20000357'
			},
			{
				'CATEGORY': 'Toy Trains HO Scale', 
				'ONSALE': 'No', 
				'SCALE': '1/87', 
				'ENDOFLIFE': 'DISC', 
				'PRICE': '29.95000', 
				'COST': '16.18000', 
				'DITEM': 'http://www.emerydistributors.com/Images/ProductImages/15020000426.jpg', 
				'INSTOCK': None, 
				'DESCRIP': 'HO 25,500g Tank Car PLMX #25133', 
				'VPARTNO': 'ATL20000426'
			},
			None
		]
		
		results = list(self.plugin.get_items(supplier_catalog))
		self.assertEqual(expected, results)

	def test_issue_date(self):
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
				'CATEGORY': 'Toy Slot Cars', 
				'ONSALE': 'No', 
				'SCALE': None, 
				'ENDOFLIFE': None, 
				'PRICE': '9.50000', 
				'COST': '5.13000', 
				'DITEM': 'http://www.emerydistributors.com/Images/ProductImages/1071012.jpg', 
				'INSTOCK': None, 
				'DESCRIP': 'Track Clip/10pk', 
				'VPARTNO': 'AFX1012'
			},
			{
				'CATEGORY': 'Toy Trains HO Scale', 
				'ONSALE': 'Yes', 
				'SCALE': '1/87', 
				'ENDOFLIFE': None, 
				'PRICE': '35.95000', 
				'COST': '14.38000', 
				'DITEM': 'http://www.emerydistributors.com/Images/ProductImages/15020000357.jpg', 
				'INSTOCK': 'YES', 
				'DESCRIP': "HO 89'Flat Erie Western #250051", 
				'VPARTNO': 'ATL20000357'
			},
			{
				'CATEGORY': 'Toy Trains HO Scale', 
				'ONSALE': 'No', 
				'SCALE': '1/87', 
				'ENDOFLIFE': 'DISC', 
				'PRICE': '29.95000', 
				'COST': '16.18000', 
				'DITEM': 'http://www.emerydistributors.com/Images/ProductImages/15020000426.jpg', 
				'INSTOCK': None, 
				'DESCRIP': 'HO 25,500g Tank Car PLMX #25133', 
				'VPARTNO': 'ATL20000426'
			},
			None
		]

		expected = [
			{
				'category_identifier': 'Toy Slot Cars',
				'cost': Decimal('5.13000'),
				'manufacturer_identifier': 'AFX',
				'name': 'Track Clip/10pk',
				'phased_out': False,
				'product_identifier': '1012',
				'retail': Decimal('9.50000'),
				'scale_identifier': None,
				'special': False,
				'special_cost': Decimal('0'),
				'stock': False
			},
			{
				'category_identifier': 'Toy Trains HO Scale',
				'cost': Decimal('0'),
				'manufacturer_identifier': 'ATL',
				'name': 'HO 89\'Flat Erie Western #250051',
				'phased_out': False,
				'product_identifier': '20000357',
				'retail': Decimal('35.95000'),
				'scale_identifier': '1/87',
				'special': True,
				'special_cost': Decimal('14.38000'),
				'stock': True
			},
			{
				'category_identifier': 'Toy Trains HO Scale',
				'cost': Decimal('16.18000'),
				'manufacturer_identifier': 'ATL',
				'name': 'HO 25,500g Tank Car PLMX #25133',
				'phased_out': True,
				'product_identifier': '20000426',
				'retail': Decimal('29.95000'),
				'scale_identifier': '1/87',
				'special': False,
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

