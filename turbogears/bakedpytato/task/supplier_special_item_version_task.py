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
import hashlib
import logging 
import random
import re
from datetime import datetime

### Extended Library
from pybloom import ScalableBloomFilter
from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
import transaction

### Application Library
from bakedpytato import model
from bakedpytato.model import metadata, DBSession
from bakedpytato.model import SupplierSpecialItemFieldModel
#from bakedpytato.model import SupplierSpecialItemVersionModel
from bakedpytato.model import SupplierSpecialModel
from bakedpytato.task.base_supplier_special_task import BaseSupplierSpecialTask


logger = logging.getLogger(__name__)


class SupplierSpecialItemVersionTask(BaseSupplierSpecialTask):
	
	def load(self):
		"""Load"""
		logger.debug("Begin load()")
		self.load_all(limit=10)
		logger.debug("End load()")
	
	def load_all(self, limit=None, item_versions_loaded=None, supplier_id=None):
		"""Load All"""
		logger.debug("Begin load_all(limit=%s, item_versions_loaded=%s)", limit, item_versions_loaded)
		self.ts = self.term_stat('SupplierSpecialItemVersion Load')
		tx = transaction.get()

		try:
			self.plugins = self.load_plugins()
			query = DBSession.query(SupplierSpecialModel)
			alt_query = query.filter(SupplierSpecialModel.supplier_special_item_versions_loaded == None)
			
			if alt_query.count() > 0:
				query = alt_query.order_by(desc(SupplierSpecialModel.begin_date))
			else:
				query = query.order_by(SupplierSpecialModel.supplier_special_item_versions_loaded.nullsfirst())
			del alt_query

			if supplier_id is not None:
				query = query.filter(SupplierSpecialModel.supplier_id == supplier_id)
			else:
				query = query.filter(SupplierSpecialModel.supplier_id != None)

			if limit is not None:
				query = query.limit(limit)

			self.ts['total'] = query.count()
			for supplier_special in query.yield_per(10):
				self.load_one(supplier_special)
				supplier_special.supplier_special_item_versions_loaded = datetime.now()
				if self.ts['done'] % 1000 == 0 :
					DBSession.flush()
				self.ts['done'] += 1
		except Exception:
			logger.exception('Caught Exception: ')
			tx.abort()
		finally:
			self.ts.finish()
		transaction.commit()
		logger.debug("End load_all()")
		
	def load_one(self, supplier_special):
		self.load_from_supplier_special(supplier_special)
			
	def load_from_supplier_special(self, supplier_special):
		if not supplier_special.supplier_special_filter_id in self.plugins:
			logger.warning("Plugin %s Not Found For SupplierSpecial %s", supplier_special.supplier_special_filter_id, supplier_special.id)
			return None
		plug = self.plugins[supplier_special.supplier_special_filter_id]
		self.ts['sub_done'] = 0
		row_number = 0

		for row in plug.get_items(supplier_special):
			self.ts['sub_done'] += 1
			row_number += 1
			supplier_special_item_field = self.load_supplier_special_item_field(supplier_special, row)
			self.load_supplier_special_item_version(supplier_special, supplier_special_item_field, row_number)

	def load_supplier_special_item_field(self, supplier_special, row):
		if row is not None:
			j = SupplierSpecialItemFieldModel.encode_json(row)
		else:
			j = None

		if j is None:
			supplier_special_item_field = None
		else:
			checksum = hashlib.sha1(j).hexdigest()
			plug = self.plugins[supplier_special.supplier_special_filter_id]
		
			query = DBSession.query(SupplierSpecialItemFieldModel)
			query = query.filter(SupplierSpecialItemFieldModel.checksum == checksum)
			try:
				supplier_special_item_field = query.one()
			except NoResultFound:
				supplier_special_item_field = SupplierSpecialItemFieldModel()
				DBSession.add(supplier_special_item_field)
			supplier_special_item_field.fields = j.encode('utf-8')
			supplier_special_item_field.checksum = checksum
			supplier_special_item_field.supplier_id = supplier_special.supplier_id
			supplier_special_item_field.supplier_special_filter_id = plug.supplier_special_filter_id()
		return supplier_special_item_field

	def load_supplier_special_item_version(self, supplier_special, supplier_special_item_field, row_number):
		plug = self.plugins[supplier_special.supplier_special_filter_id]
		model_name = plug.version_model()  + 'Model'
		VersionModel = getattr(model, model_name)
		query = DBSession.query(VersionModel)
		query = query.filter(VersionModel.supplier_special_id == supplier_special.id)
		query = query.filter(VersionModel.row_number == row_number)
		
		if supplier_special_item_field is None:
			query.delete()
			supplier_special_item_version = None
		else:
			try:
				supplier_special_item_version = query.one()
			except NoResultFound:
				supplier_special_item_version = VersionModel()
				DBSession.add(supplier_special_item_version)
		
			supplier_special_item_version.supplier_special_id = supplier_special.id
			supplier_special_item_version.supplier_special_item_field_id = supplier_special_item_field.id
			supplier_special_item_version.supplier_special_filter_id = plug.supplier_special_filter_id()
			supplier_special_item_version.row_number = row_number
			#supplier_special_item_version.effective = supplier_special.issue_date
		return supplier_special_item_version

	def update(self):
		logger.debug("Begin update()")
		self.update_all()
		logger.debug("End update()")

	#def update_all(self):
		#logger.debug("Begin update_all()")
		#self.ts = self.term_stat("SupplierSpecialItemVersion update")
		#tx = transaction.get()
		#try:
			#self.plugins = self.load_plugins()

			#query = DBSession.query(SupplierSpecialModel)
			#self.ts['total'] = query.count()

			#for plug in self.plugins.itervalues():
				#supplier_special_filter_id = plug.supplier_special_filter_id()
				#model_name = plug.version_model()  + 'Model'
				#VersionModel = getattr(model, model_name)
				#query = DBSession.query(SupplierSpecialModel)
				#query = query.filter(SupplierSpecialModel.supplier_special_filter_id == supplier_special_filter_id)
				#for supplier_special in query.yield_per(1):
					#self.update_from_supplier_special(supplier_special, VersionModel)
					#self.ts['done'] += 1
					#DBSession.flush()
		#except Exception:
			#logger.exception('Caught Exception: ')
			#tx.abort()
		#finally:
			#self.ts.finish()
		#transaction.commit()
		#logger.debug("End update_all()")
	
	#def update_from_supplier_special(self, supplier_special, VersionModel):
		#query = DBSession.query(VersionModel)
		#query = query.filter(VersionModel.supplier_special_id == supplier_special.id)
		#query = query.filter(VersionModel.effective != supplier_special.issue_date)
		#c = query.count()
		#self.ts['sub_done'] = c
		#if c > 0:
			#values = dict()
			#values['effective'] = supplier_special.issue_date
			#values['updated'] = datetime.now()
			#query.update(values, synchronize_session=False)

	def vacuum(self):
		logger.debug('Begin vacuum()')
		self.vacuum_all(limit=10000)
		logger.debug('End vacuum()')
		
		
	def vacuum_all(self, limit=None):
		logger.debug('Begin vacuum_all(limit=%s)', limit)
		self.plugins = self.load_plugins()
		ts = self.term_stat('SupplierSpecialItemVersion Vacuum', len(self.plugins))
		tx = transaction.get()
		
		try:
			#s = set()
			s = ScalableBloomFilter()
			query = DBSession.query(SupplierSpecialModel.id)
			for (supplier_special_id, ) in query.yield_per(100):
				s.add(supplier_special_id)
			
			for plug in self.plugins.itervalues():
				supplier_special_filter_id = plug.supplier_special_filter_id()
				model_name = plug.version_model()  + 'Model'
				VersionModel = getattr(model, model_name)
				query = DBSession.query(VersionModel)
				if limit:
					query = query.order_by(VersionModel.vacuumed.nullsfirst())
					query = query.limit(limit)

				ts['sub_done'] = 0
				ts['sub_total'] = query.count()
				for supplier_special_item_version in query.yield_per(10):
					if supplier_special_item_version.supplier_special_id not in s:
						logger.debug("Deleting %s %s", model_name, supplier_special_item_version.id)
						DBSession.delete(supplier_special_item_version)
					ts['sub_done'] += 1
					if ts['sub_done'] % 1000 == 0:
						DBSession.flush()
				DBSession.flush()
				ts['done'] += 1
		except Exception:
			logger.exception('Caught Exception: ')
			tx.abort()
		finally:
			ts.finish()
		transaction.commit()
		logger.debug('End vacuum_all()')
