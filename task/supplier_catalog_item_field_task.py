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
#import hashlib
#import json
import logging 
import re
from decimal import *

#Extended Library
from sqlalchemy.orm.exc import NoResultFound

#Application Library
import cfg
#import model
from model import SupplierCatalogItemFieldModel
#from model import SupplierCatalogItemFieldModel
#from model import SupplierCatalogModel
from priceutil import decimal_round

#This Package
from task.base_supplier_catalog_task import BaseSupplierCatalogTask

logger = logging.getLogger(__name__)

class SupplierCatalogItemFieldTask(BaseSupplierCatalogTask):
	
	field_names = [
		'advanced',
		'availability_indefinite',
		'available',
		'category_identifier',
		'cost',
		'manufacturer_identifier', 
		'name', 
		'phased_out',
		'product_identifier',
		'retail', 
		'scale_identifier',
		'special_cost',
		'stock',
		'to_be_announced'
	]
	
	def update_all(self):
		"""Update All"""
		logger.debug("Begin update_all()")
		self.session.begin(subtransactions=True)
		self.plugins = self.load_plugins()
		query = self.session.query(SupplierCatalogItemFieldModel)
		self.ts = self.term_stat('SupplierCatalogItemField Update All', query.count())
		for supplier_catalog_item_field in query.yield_per(1000):
			#self.session.begin(subtransactions=True)
			self.update_one(supplier_catalog_item_field)
			if self.ts['done'] % 1000 == 0:
				self.session.flush()
			#self.session.commit()
			self.ts['done'] += 1
		self.session.commit()
		self.ts.finish()
		logger.debug("End load_all()")
			
	def update_one(self, supplier_catalog_item_field):
		if not supplier_catalog_item_field.supplier_catalog_filter_id in self.plugins:
			logger.warning("Plugin %s Not Found", supplier_catalog_item_field.supplier_catalog_filter_id)
			return None
		plug = self.plugins[supplier_catalog_item_field.supplier_catalog_filter_id]
		fields = supplier_catalog_item_field.get_fields()
		data = plug.update_fields(fields)
		if data is not None:
			#print "Fields:", fields
			#print "Data:", data
			for field_name in self.field_names:
				if field_name in data:
					field = data[field_name]
					if isinstance(field, basestring):
						field = field.strip()
						field = re.sub(r'\s\s+', ' ', field) #multiple spaces become single
						
						
						if field_name == 'product_identifier':
							field = field.lstrip('0')
					elif isinstance(field, Decimal):
						if field_name in ['cost', 'special_cost']:
							field = decimal_round(field, cfg.cost_decimals)

						if field_name in ['retail']:
							field = decimal_round(field, cfg.retail_decimals)

					setattr(supplier_catalog_item_field, field_name, field)
				else:
					setattr(supplier_catalog_item_field, field_name, None)
		else:
			#logger.warning("Plugin returned empty data %s %s", supplier_catalog_item_field.supplier_catalog_filter_id, fields)
			for field_name in self.field_names:
				setattr(supplier_catalog_item_field, field_name, None)

