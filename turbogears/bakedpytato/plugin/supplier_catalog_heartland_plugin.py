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
#Pragma
from __future__ import unicode_literals

#Standard Library
import csv
import logging 
import re
from datetime import datetime
from decimal import *

#Extended Library

#Application Library

#This Package
from plugin.base_supplier_catalog_plugin import BaseSupplierCatalogPlugin

logger = logging.getLogger(__name__)

class SupplierCatalogHeartlandPlugin(BaseSupplierCatalogPlugin):

	default_encoding = 'windows-1252'
	
	column_names = ['SKU', 'Name', 'Retail']
	
	#Effective 2011-03-22
	discount = '44.3';
	discount_by_manufacturer = {
		'ACU':'44.3', 'ATL':'44.3', 'ARI':'30.9', 'BAC':'48.5',
		'BLM':'44.3', 'BOW':'40.0', 'BLI':'31.9', 'BFS':'40.2',
		'CAB':'38.1', 'CIR':'44.3', 'MWI':'44.3', 'FVM':'44.3',
		'GGT':'34.5', 'GCR':'40.0', 'IMX':'48.5', 'KAD':'44.3',
		'KAT':'44.3', 'MIE':'40.2', 'MNT':'38.1', 'MDP':'48.5',
		'MRC':'44.3', 'NCE':'40.2', 'PCO':'44.3', 'PCM':'31.9',
		'RAP':'44.3', 'RAT':'38.1', 'SWH':'44.3', 'TCS':'39.2',
		'WHT':'41.0', 'WIL':'38.1', 'AMB':'44.3', 'AAC':'44.3',
		'CHO':'44.3', 'DPM':'38.1', 'EVG':'44.3', 'EXL':'53.6',
		'FLO':'48.5', 'HLB':'44.3', 'K+S':'44.3', 'KAL':'44.3',
		'KMT':'38.1', 'LAB':'44.3', 'MMZ':'44.3', 'MID':'44.3',
		'MSE':'38.1', 'PAC':'48.5', 'PKS':'44.3', 'PIN':'44.3',
		'PLS':'44.3', 'RIX':'44.3', 'ROB':'50.5', 'SEX':'44.3',
		'SMA':'44.3', 'SII':'48.5', 'SQU':'44.3', 'TAM':'48.5',
		'TNX':'48.5', 'TES':'48.5', 'XAC':'50', 'XUR':'44.3',
		'WOO':'44.3'
	}
		
	discount_by_sku = {
		#Atlas Bulk Track	48.5
		'ATL1001049':'48.5',
		'ATL1001067':'48.5',
		'ATL155':'48.5',
		'ATL24':'48.5',
		'ATL2513':'48.5',
		'ATL2515':'48.5',
		'ATL2516':'48.5',
		'ATL2517':'48.5',
		'ATL2534':'48.5',
		'ATL410':'48.5',
		'ATL411':'48.5',
		'ATL412':'48.5',
		'ATL90150':'48.5',
		'ATL90151':'48.5',
		'ATL90152':'48.5',
		'ATL90153':'48.5',
		
		#Atlas O	30.9
		#Atlas Trainman	30.9
		#BLMA Brass	26.3
		#BLI Brass, Hybrid	21
		#BLI Blueline	49.5
		#BLI Paragon 2	41
		#Circuitron Tortoise Machines 41.6
		'CIR6000':'41.6',
		'CIR6006':'41.6',
		'CIR6012':'41.6',
		#Kadee '#' noted items	25
		#Kato Special Items	23.7
		#Model Power Tunnels	40
		#Precision Craft Models Brass	21
	}
	
	skipable = [
		'ATL0531', 
		'CASH', 
		'DASB', 
		'DASR', 
		'DROP SHIP',
		'FRGT',
		'FRGTADJ',
		'LIONEL COOP'
	]
	
	scales = [
		r'^(HO)\s',
		r'\s(HO)\s',
		r'^HOn3\s',
		r'^\sHOn3\s',
		r'^N\s',
		r'\sN\s',
		r'^O\s',
		r'\sO\s',
	]

	def match_file_import(self, file_import):
		if re.search('lock', file_import.name):
			return False
		if not re.search('hhwonhand-\d{14}.csv', file_import.name):
			return False
		magic = file_import.magic()
		if magic['mime'] != 'text/plain':
			return False
		if magic['magic'] != 'ISO-8859 text, with CRLF line terminators':
			return False
		return True
		
	def get_items(self, supplier_catalog):
		expected_row_len = len(self.column_names)
		content = supplier_catalog.file_import.content
		lines = re.split("\n", content)
		reader = csv.reader(lines, delimiter=bytes(','))
		for row in reader:
			
			if row is None or row == []:
				yield None
				continue
			
			if len(row) != expected_row_len:
				logger.warning("Row has incorrect length: expected %i, got %i '%s'", expected_row_len, len(row), row)
				yield None
				continue

			item = dict()
			i = 0
			for column_name in self.column_names:
				field = row[i]
				field = field.strip()
				item[column_name] = field
				i += 1
			item = self.recode(item)
			yield item
		
	def issue_date(self, file_import):
		m = re.search('(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2}).csv$', file_import.name)
		if m:
			return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6)))

		logger.warning("Failed to convert issue_date for %s", file_import.name)
		return file_import.effective

	def update_fields(self, fields):
		"""Update Field"""

		if fields is None:
			logger.warning("Fields is empty")
			return None

		data = dict()
		
		if 'SKU' in fields:
			if fields['SKU'] in self.skipable:
				return None
			m = re.match(r'^(...)(.*)$', fields['SKU'])
			if m:
				data['manufacturer_identifier'] = m.group(1)
				data['product_identifier'] = m.group(2)

		data['stock'] = True
		
		data['scale'] = None

		if 'Name' in fields:
			data['name'] = fields['Name']
			
			for scale in self.scales:
				m = re.search(scale, data['name'])
				if m:
					data['scale'] = m.group(0).strip()
			
			
		if 'Retail' in fields:
			data['retail'] = Decimal(fields['Retail'])
			if fields['SKU'] in self.discount_by_sku:
				discount = self.discount_by_sku[fields['SKU']]
				
				
			##FIXME This shouldn't be hardcoded
			elif data['manufacturer_identifier'] == 'KAD':
				m = re.match(r'^\#', data['name'])
				if m:
					discount = '25'
				else:
					discount = '44.3'
			elif data['manufacturer_identifier'] in self.discount_by_manufacturer:
				discount = self.discount_by_manufacturer[data['manufacturer_identifier']]

			else:
				discount = self.discount

			ratio = (Decimal('100') - Decimal(discount)) / Decimal('100')
			data['cost'] = data['retail'] * ratio
		return data
