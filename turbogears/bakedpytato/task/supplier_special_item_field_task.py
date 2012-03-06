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
### Pragma
from __future__ import unicode_literals

### Standard Library
import logging 
import re
from decimal import Decimal
from datetime import datetime, timedelta
import transaction

###Extended Library
from pybloom import BloomFilter
from sqlalchemy.orm.exc import NoResultFound

###Application Library
from bakedpytato import cfg, model
from bakedpytato.model import metadata, DBSession
from bakedpytato.model import SupplierSpecialItemFieldModel
from bakedpytato.task.base_supplier_special_task import BaseSupplierSpecialTask
from bakedpytato.util.price_util import decimal_round


logger = logging.getLogger(__name__)

class SupplierSpecialItemFieldTask(BaseSupplierSpecialTask):
	
	field_names = [
		'manufacturer_identifier', 
		'normal_cost', 
		'normal_retail',
		'product_identifier',
		'special_cost',
		'special_ratio', 
		'special_retail', 
	]

	def update(self):
		return self.update_all(limit=10000, time_limit=timedelta(hours=1))
	
	def update_all(self, limit=None, time_limit=None):
		"""Update All"""
		logger.debug("Begin update_all(limit=%s)", limit)
		tx = transaction.get()
		self.ts = self.term_stat('SupplierSpecialItemField Update')
		start_time = datetime.now()
		try:
			self.plugins = self.load_plugins()
			query = DBSession.query(SupplierSpecialItemFieldModel)
			if limit is not None:
				query = query.order_by(SupplierSpecialItemFieldModel.updated.nullsfirst())
				query = query.limit(limit)
			self.ts['total'] = query.count()
			for supplier_special_item_field in query.yield_per(10000):
				self.update_one(supplier_special_item_field)
				if self.ts['done'] % 10000 == 0:
					DBSession.flush()
				if time_limit is not None:
					if datetime.now() > start_time + time_limit:
						logger.info("Reached Time Limit at %i of %i", ts['done'], ts['total'])
						break;
				self.ts['done'] += 1
			del query
		except Exception:
			logger.exception("Caught Exception: ")
			tx.abort()
		finally:
			self.ts.finish()
		transaction.commit()
		logger.debug("End update_all()")
			
	def update_one(self, supplier_special_item_field):
		if not supplier_special_item_field.supplier_special_filter_id in self.plugins:
			logger.warning("Plugin '%s' Not Found", supplier_special_item_field.supplier_special_filter_id)
			return None
		plug = self.plugins[supplier_special_item_field.supplier_special_filter_id]
		fields = supplier_special_item_field.get_fields()
		
		data = plug.update_fields(fields)
		if data is not None:
			print "Fields:", fields
			print "Data:", data
			for field_name in self.field_names:
				if field_name in data:
					field = data[field_name]
					if isinstance(field, basestring):
						field = field.strip()
						field = re.sub(r'\s\s+', ' ', field) #multiple spaces become single
						if field_name in ['product_identifier', 'manufacturer_identifier']:
							field = field.lstrip('0')
					elif isinstance(field, Decimal):
						if field_name in ['cost', 'special_cost']:
							field = decimal_round(field, cfg.cost_decimals)

						if field_name in ['retail']:
							field = decimal_round(field, cfg.retail_decimals)

					setattr(supplier_special_item_field, field_name, field)
					print 'SETATTR', supplier_special_item_field, field_name, field
				else:
					#logger.warning("Plugin returned empty data for %s %s", field_name, fields)
					setattr(supplier_special_item_field, field_name, None)
		else:
			logger.warning("Plugin returned empty data %s %s %s", supplier_special_item_field.id, supplier_special_item_field.supplier_special_filter_id, fields)
			for field_name in self.field_names:
				setattr(supplier_special_item_field, field_name, None)
		supplier_special_item_field.updated = datetime.now()


	def vacuum(self):
		logger.debug('Begin vacuum()')
		self.vacuum_all(limit=100000, time_limit=timedelta(hours=1))
		logger.debug('End vacuum()')

	def vacuum_all(self, limit=None, time_limit=None, unupdated=False):
		logger.debug('Begin vacuum_all(limit=%s, time_limit=%s, unupdated=%s)', limit, time_limit, unupdated)
		##TODO delete SCIFields with SCFilterId not found in SCFilter

		self.plugins = self.load_plugins()
		self.ts = self.term_stat('SupplierSpecialItemFields Vacuum', len(self.plugins))
		now = start_time = datetime.now()
		try:
			transaction.begin()
			for plug in self.plugins.itervalues():
				supplier_special_filter_id = plug.supplier_special_filter_id()
				
				### Generate a bloom filter set of SCIF id's in VersionModel
				model_name = plug.version_model()  + 'Model'
				VersionModel = getattr(model, model_name)
				query = DBSession.query(VersionModel.supplier_special_item_field_id)
				s = BloomFilter(capacity=query.count() + 1)
				self.ts['sub_total'] = query.count()
				for (supplier_special_item_field_id, )  in query.yield_per(100):
					s.add(supplier_special_item_field_id)
					self.ts['sub_done'] += 1
				del query
				
				### Iterate through SCIFields, deleting any that don't appear in the bloom filter.
				query = DBSession.query(SupplierSpecialItemFieldModel)
				query = query.filter(SupplierSpecialItemFieldModel.supplier_special_filter_id == supplier_special_filter_id)
				if unupdated is not True:
					query = query.filter(SupplierSpecialItemFieldModel.updated != None)
				
				if limit is not None:
					query = query.order_by(SupplierSpecialItemFieldModel.vacuumed.nullsfirst())
					query = query.limit(limit)
					logger.debug("LIMIT %i, supplier_special_filter_id %s", limit, supplier_special_filter_id)
				self.ts['sub_done'] = 0
				self.ts['sub_total'] = query.count()
				for supplier_special_item_field in query.yield_per(100):
					if supplier_special_item_field.id not in s:
						logger.debug("Deleting SupplierSpecialItemField %s", supplier_special_item_field.id)
						DBSession.delete(supplier_special_item_field)
					else:
						supplier_special_item_field.vacuumed = now
					if self.ts['sub_done'] % 1000 == 0:
						DBSession.flush()
					self.ts['sub_done'] += 1
				del query
				DBSession.flush()
				if time_limit is not None:
					if datetime.now() > start_time + time_limit:
						logger.info("Reached Time Limit at %i of %i", self.ts['done'], self.ts['total'])
						transaction.commit()
						break;
				self.ts['done'] += 1
			transaction.commit()
		except Exception:
			logger.exception("Caught Exception: ")
			transaction.abort()
		finally:
			self.ts.finish()
		logger.debug('End vacuum()')
