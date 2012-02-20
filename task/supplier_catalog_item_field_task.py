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
import random

#Extended Library
from sqlalchemy.orm.exc import NoResultFound

#Application Library
import cfg
import model
from model import SupplierCatalogItemFieldModel
#from model import SupplierCatalogItemFieldModel
#from model import SupplierCatalogModel
from util.price_util import decimal_round


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

	def update(self):
		return self.update_all()
	
	def update_all(self):
		"""Update All"""
		logger.debug("Begin update_all()")
		self.session.begin(subtransactions=True)
		try:
			self.plugins = self.load_plugins()
			query = self.session.query(SupplierCatalogItemFieldModel)
			self.ts = self.term_stat('SupplierCatalogItemField Update All', query.count())
			for supplier_catalog_item_field in query.yield_per(1000):
				self.update_one(supplier_catalog_item_field)
				if self.ts['done'] % 1000 == 0:
					self.session.flush()
				self.ts['done'] += 1
			self.session.commit()
		except Exception:
			logger.exception("Caught Exception: ")
			if self.session.transaction is not None:
				self.session.rollback()
		finally:
			self.ts.finish()
		logger.debug("End update_all()")
			
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
						if field_name in ['product_identifier', 'manufacturer_identifier', 'category_identifier']:
							field = field.lstrip('0')
					elif isinstance(field, Decimal):
						if field_name in ['cost', 'special_cost']:
							field = decimal_round(field, cfg.cost_decimals)

						if field_name in ['retail']:
							field = decimal_round(field, cfg.retail_decimals)

					setattr(supplier_catalog_item_field, field_name, field)
				else:
					#logger.warning("Plugin returned empty data for %s %s", field_name, fields)
					setattr(supplier_catalog_item_field, field_name, None)
		else:
			logger.warning("Plugin returned empty data %s %s %s", supplier_catalog_item_field.id, supplier_catalog_item_field.supplier_catalog_filter_id, fields)
			for field_name in self.field_names:
				setattr(supplier_catalog_item_field, field_name, None)

	def vacuum(self):
		logger.debug('Begin vacuum()')
		self.vacuum_all(rand_limit=100)
		logger.debug('End vacuum()')

	def vacuum_all(self, rand_limit=None):
		logger.debug('Begin vacuum_all(rand_limit=%s)', rand_limit)
		##TODO delete SCIFields with SCFilterId not found in SCFilter
		
		try:
		
			self.plugins = self.load_plugins()

			self.session.begin()
			
			self.ts = self.term_stat('SupplierCatalogItemFields Vacuum', len(self.plugins))
			
			for plug in self.plugins.itervalues():
				supplier_catalog_filter_id = plug.supplier_catalog_filter_id()
				model_name = plug.version_model()  + 'Model'
				VersionModel = getattr(model, model_name)
				query = self.session.query(SupplierCatalogItemFieldModel)
				query = query.filter(SupplierCatalogItemFieldModel.supplier_catalog_filter_id == supplier_catalog_filter_id)
				
				if rand_limit is not None:
					c = query.count() - rand_limit
					if c < 0:
						c = 0
					offset = random.randint(0, c)
					query = query.offset(offset)
					query = query.limit(rand_limit)
					logger.debug("LIMIT %i, OFFSET %i, supplier_catalog_filter_id %s", rand_limit, offset, supplier_catalog_filter_id)
				
				self.ts['sub_done'] = 0
				for supplier_catalog_item_field in query.yield_per(100):
					count = self.vacuum_count(supplier_catalog_item_field, VersionModel)
					if count > 0:
						supplier_catalog_item_field.supplier_catalog_item_version_count = count
					else:
						logger.debug("Deleting SupplierCatalogItemField %s", supplier_catalog_item_field.id)
						self.session.delete(supplier_catalog_item_field)
					self.ts['sub_done'] += 1
				self.ts['done'] += 1
			self.session.commit()
		except Exception:
			logger.exception("Caught Exception: ")
			if self.session.transaction is not None:
				self.session.rollback()
		finally:
			self.ts.finish()
		logger.debug('End vacuum()')

	def vacuum_count(self, supplier_catalog_item_field, VersionModel):
		query = self.session.query(VersionModel)
		query = query.filter(VersionModel.supplier_catalog_item_field_id == supplier_catalog_item_field.id)
		count = query.count()
		logger.debug("supplier_catalog_item_field %s, count %i", supplier_catalog_item_field.id, count)
		return count
