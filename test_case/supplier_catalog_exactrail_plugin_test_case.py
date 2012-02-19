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
from plugin.supplier_catalog_exactrail_plugin import SupplierCatalogExactrailPlugin
from model import *

class SupplierCatalogExactrailPluginTestCase(unittest.TestCase):
	
	def setUp(self):
		self.maxDiff = None
		self.file_import = FileImportModel()
		self.supplier_catalog_filter = SupplierCatalogFilterModel()
		self.plugin = SupplierCatalogExactrailPlugin(self.supplier_catalog_filter)
		
	def test_match_file_import(self):
		self.file_import.name = "blargh"
		self.file_import.content = "blargh"
		
		result = self.plugin.match_file_import(self.file_import)
		self.assertFalse(result)

		self.file_import.name = "blarghexactrailblargh"
		result = self.plugin.match_file_import(self.file_import)
		self.assertTrue(result)

		self.file_import.name = "20100101.csv"
		result = self.plugin.match_file_import(self.file_import)
		self.assertTrue(result)

	def test_get_items(self):
		self.file_import.content = ""
		supplier_catalog = SupplierCatalogModel()
		supplier_catalog.file_import = self.file_import
		for result in self.plugin.get_items(supplier_catalog):
			self.assertIsNone(result)

		c = [
			'UPC/SKU,Description,Road Name,Road #s\',MSRP,Stock,Dealer',
			'EE-1010-4,PC&F 6033 cu. ft. Hy-Cube Box Car,SSW,61147,$27.95 ,< 25 Call,$16.77 ',
			'EN-50300-6,Trinity 64\' TRINCool Refrigerated Box Car : UP/ARMN : 111285,UP/ARMN,111285,$29.95 ,In Stock,$17.97 ',
			'EP-80171-4,PS-2CD 4427 Covered Hopper,Cargill/TLDX,2841,$37.95,In Stock,$22.77 ',
			'EPS-90053-6,B&O M-53 Wagontop Box Car,B&O,380696,$32.95 ,In Stock,$19.77 ',
			'ET-110,"100 Ton ASF Ride Control trks 36"" fine",None,None,$9.95 ,In Stock,$5.97 ',
			'EW-211,"33"" Brass Wheelsets fine (12-pack)",None,None,$9.95 ,In Stock,$5.97 ',
			'EWN-301,33 Inch Brass Wheelsets (12-pack),None,None,$9.95 ,OOS,$5.97 ',
			'EX-1401-6,FMC 4000 Gondola, RTIX,437,$22.95 ,In Stock,$13.77 ',
			''
		]
		self.file_import.content = "\n".join(c)
		
		expected = [
			{
				'DESCRIPTION': 'PC&F 6033 cu. ft. Hy-Cube Box Car', 
				'UPC/SKU': 'EE-1010-4', 
				'ROAD NAME': 'SSW', 
				"ROAD #S'": '61147', 
				'DEALER': '$16.77 ', 
				'MSRP': '$27.95 ', 
				'STOCK': '< 25 Call'
			},
			{
				'DEALER': '$17.97 ',
				'DESCRIPTION': "Trinity 64' TRINCool Refrigerated Box Car : UP/ARMN : 111285",
				'MSRP': '$29.95 ',
				"ROAD #S'": '111285',
				'ROAD NAME': 'UP/ARMN',
				'STOCK': 'In Stock',
				'UPC/SKU': 'EN-50300-6'
			},
			{
				'DEALER': '$22.77 ',
				'DESCRIPTION': 'PS-2CD 4427 Covered Hopper',
				'MSRP': '$37.95',
				"ROAD #S'": '2841',
				'ROAD NAME': 'Cargill/TLDX',
				'STOCK': 'In Stock',
				'UPC/SKU': 'EP-80171-4'
			},
			{
				'DEALER': '$19.77 ',
				'DESCRIPTION': 'B&O M-53 Wagontop Box Car',
				'MSRP': '$32.95 ',
				"ROAD #S'": '380696',
				'ROAD NAME': 'B&O',
				'STOCK': 'In Stock',
				'UPC/SKU': 'EPS-90053-6'
			},
			{
				'DEALER': '$5.97 ',
				'DESCRIPTION': '100 Ton ASF Ride Control trks 36" fine',
				'MSRP': '$9.95 ',
				"ROAD #S'": 'None',
				'ROAD NAME': 'None',
				'STOCK': 'In Stock',
				'UPC/SKU': 'ET-110'
			},
			{
				'DEALER': '$5.97 ',
				'DESCRIPTION': '33" Brass Wheelsets fine (12-pack)',
				'MSRP': '$9.95 ',
				"ROAD #S'": 'None',
				'ROAD NAME': 'None',
				'STOCK': 'In Stock',
				'UPC/SKU': 'EW-211'
			},
			{
				'DEALER': '$5.97 ',
				'DESCRIPTION': '33 Inch Brass Wheelsets (12-pack)',
				'MSRP': '$9.95 ',
				"ROAD #S'": 'None',
				'ROAD NAME': 'None',
				'STOCK': 'OOS',
				'UPC/SKU': 'EWN-301'
			},
			{
				'DEALER': '$13.77 ',
				'DESCRIPTION': 'FMC 4000 Gondola',
				'MSRP': '$22.95 ',
				"ROAD #S'": '437',
				'ROAD NAME': ' RTIX',
				'STOCK': 'In Stock',
				'UPC/SKU': 'EX-1401-6'
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

		self.file_import.name = "19770901.csv"
		result = self.plugin.issue_date(self.file_import)
		self.assertEqual(result, datetime.datetime(1977, 9, 1, 0, 0, 0))

		#pass an invalid date. 
		#Expected result: an error is logged, and file_import.effective is returned instead.
		self.file_import.name = "20009999.csv"
		result = self.plugin.issue_date(self.file_import)
		self.assertEqual(result, self.file_import.effective)


	def test_update_fields(self):
		fieldsets = [
			{
				'DESCRIPTION': 'PC&F 6033 cu. ft. Hy-Cube Box Car', 
				'UPC/SKU': 'EE-1010-4', 
				'ROAD NAME': 'SSW', 
				"ROAD #S'": '61147', 
				'DEALER': '$16.77 ', 
				'MSRP': '$27.95 ', 
				'STOCK': '< 25 Call'
			},
			{
				'DEALER': '$17.97 ',
				'DESCRIPTION': "Trinity 64' TRINCool Refrigerated Box Car : UP/ARMN : 111285",
				'MSRP': '$29.95 ',
				"ROAD #S'": '111285',
				'ROAD NAME': 'UP/ARMN',
				'STOCK': 'In Stock',
				'UPC/SKU': 'EN-50300-6'
			},
			{
				'DEALER': '$22.77 ',
				'DESCRIPTION': 'PS-2CD 4427 Covered Hopper',
				'MSRP': '$37.95',
				"ROAD #S'": '2841',
				'ROAD NAME': 'Cargill/TLDX',
				'STOCK': 'In Stock',
				'UPC/SKU': 'EP-80171-4'
			},
			{
				'DEALER': '$19.77 ',
				'DESCRIPTION': 'B&O M-53 Wagontop Box Car',
				'MSRP': '$32.95 ',
				"ROAD #S'": '380696',
				'ROAD NAME': 'B&O',
				'STOCK': 'In Stock',
				'UPC/SKU': 'EPS-90053-6'
			},
			{
				'DEALER': '$5.97 ',
				'DESCRIPTION': '100 Ton ASF Ride Control trks 36" fine',
				'MSRP': '$9.95 ',
				"ROAD #S'": 'None',
				'ROAD NAME': 'None',
				'STOCK': 'In Stock',
				'UPC/SKU': 'ET-110'
			},
			{
				'DEALER': '$5.97 ',
				'DESCRIPTION': '33" Brass Wheelsets fine (12-pack)',
				'MSRP': '$9.95 ',
				"ROAD #S'": 'None',
				'ROAD NAME': 'None',
				'STOCK': 'In Stock',
				'UPC/SKU': 'EW-211'
			},
			{
				'DEALER': '$5.97 ',
				'DESCRIPTION': '33 Inch Brass Wheelsets (12-pack)',
				'MSRP': '$9.95 ',
				"ROAD #S'": 'None',
				'ROAD NAME': 'None',
				'STOCK': 'OOS',
				'UPC/SKU': 'EWN-301'
			},
			{
				'DEALER': '$13.77 ',
				'DESCRIPTION': 'FMC 4000 Gondola',
				'MSRP': '$22.95 ',
				"ROAD #S'": '437',
				'ROAD NAME': ' RTIX',
				'STOCK': 'In Stock',
				'UPC/SKU': 'EX-1401-6'
			},
			None
		]

		expected = [
			{
				'name': 'PC&F 6033 cu. ft. Hy-Cube Box Car SSW 61147', 
				'manufacturer_identifier': '253', 
				'category_identifier':'PC&F 6033 cu. ft. Hy-Cube Box Car', 
				'product_identifier': 'EE-1010-4', 
				'scale_identifier': 'HO', 
				'retail': Decimal('27.95'), 
				'cost': Decimal('16.77'), 
				'special_cost': Decimal('0'), 
				'advanced': False, 
				'stock': False
			},
			{
				'cost': Decimal('17.97'), 
				'name': "Trinity 64' TRINCool Refrigerated Box Car : UP/ARMN : 111285 UP/ARMN 111285", 
				'category_identifier': 'Freight Rolling Stock', 
				'manufacturer_identifier': '253', 
				'product_identifier': 'EN-50300-6', 
				'scale_identifier': 'N', 
				'special_cost': Decimal('0'), 
				'retail': Decimal('29.95'), 
				'advanced': False, 
				'stock': True
			},
			{
				'cost': Decimal('22.77'), 
				'name': 'PS-2CD 4427 Covered Hopper Cargill/TLDX 2841', 
				'category_identifier': 'PS-2CD 4427 Covered Hopper', 
				'manufacturer_identifier': '253', 
				'product_identifier': 'EP-80171-4', 
				'scale_identifier': 'HO', 
				'special_cost': Decimal('0'), 
				'retail': Decimal('37.95'), 
				'advanced': False, 
				'stock': True
			},
			{
				'cost': Decimal('19.77'), 
				'name': 'B&O M-53 Wagontop Box Car B&O 380696', 
				'category_identifier': 'B&O M-53 Wagontop Box Car', 
				'manufacturer_identifier': '253', 
				'product_identifier': 'EPS-90053-6', 
				'scale_identifier': 'HO', 
				'special_cost': Decimal('0'), 
				'retail': Decimal('32.95'), 
				'advanced': False, 
				'stock': True
			},
			{
				'cost': Decimal('5.97'), 
				'name': '100 Ton ASF Ride Control trks 36" fine', 
				'category_identifier': 'Trucks', 
				'manufacturer_identifier': '253', 
				'product_identifier': 'ET-110', 
				'scale_identifier': 'HO', 
				'special_cost': Decimal('0'), 
				'retail': Decimal('9.95'), 
				'advanced': False, 
				'stock': True
			},
			{
				'cost': Decimal('5.97'), 
				'name': '33" Brass Wheelsets fine (12-pack)', 
				'category_identifier': 'Wheels', 
				'manufacturer_identifier': '253', 
				'product_identifier': 'EW-211', 
				'scale_identifier': 'HO', 
				'special_cost': Decimal('0'), 
				'retail': Decimal('9.95'), 
				'advanced': False, 
				'stock': True
			},
			{
				'cost': Decimal('5.97'), 
				'name': '33 Inch Brass Wheelsets (12-pack)', 
				'category_identifier': 'Wheels', 
				'manufacturer_identifier': '253', 
				'product_identifier': 'EWN-301', 
				'scale_identifier': 'N', 
				'special_cost': Decimal('0'), 
				'retail': Decimal('9.95'), 
				'advanced': False, 
				'stock': False
			},
			{
				'cost': Decimal('13.77'), 
				'name': 'FMC 4000 Gondola  RTIX 437', 
				'category_identifier': 'FMC 4000 Gondola', 
				'manufacturer_identifier': '253', 
				'product_identifier': 'EX-1401-6', 
				'scale_identifier': 'HO', 
				'special_cost': Decimal('0'), 
				'retail': Decimal('22.95'), 
				'advanced': False, 
				'stock': True
			} ,
			None
		]

		for i in xrange(len(fieldsets)):
			fieldset = fieldsets[i]
			expect = expected[i]

			result = self.plugin.update_fields(fieldset)
			self.assertEqual(result, expect)

