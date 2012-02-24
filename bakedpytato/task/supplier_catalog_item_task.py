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
#Pragma
from __future__ import unicode_literals

#Standard Library
import logging 
import uuid
import ttystatus
from datetime import datetime, timedelta
from decimal import *

#Extended Library
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import asc, desc
#from sqlalchemy.orm import in_
from pybloom import ScalableBloomFilter

#Application Library
from bakedpytato import cfg
from bakedpytato import model
from bakedpytato.model import CategoryConversionModel
from bakedpytato.model import ManufacturerModel, ManufacturerConversionModel
from bakedpytato.model import PriceControlModel
from bakedpytato.model import ProductModel, ProductConversionModel
from bakedpytato.model import ScaleModel, ScaleConversionModel
from bakedpytato.model import SupplierCatalogModel, SupplierCatalogItemModel, SupplierCatalogItemFieldModel
from bakedpytato.model.supplier_catalog_item_version_mixin import SupplierCatalogItemVersionMixin

#This Package
from bakedpytato.util.price_util import decimal_round
from bakedpytato.task.setting_task import SettingTask
from bakedpytato.task.base_supplier_catalog_task import BaseSupplierCatalogTask

logger = logging.getLogger(__name__)

class SupplierCatalogItemTask(BaseSupplierCatalogTask):

	field_names = {
		'advanced':'advanced',
		#'availability_indefinite':'availability_indefinite',
		'available':'available',
		'category_identifier':'category_identifier',
		'cost':'quantity_cost',
		#'effective':'effective',
		'manufacturer_identifier':'manufacturer_identifier', 
		'name':'name',
		'phased_out':'phased_out',
		'product_identifier':'product_identifier',
		'retail':'quantity_retail', 
		'scale_identifier':'scale_identifier',
		'special_cost':'quantity_special_cost',
		'stock':'in_stock',
		#'to_be_announced':'to_be_announced'
	}

	defaults = {
		'advanced': False,
		#'availability_indefinite': False,
		'available': None,
		'category_identifier': None,
		'cost': Decimal(0),
		'legacy_flag': 128,
		'name': None,
		'phased_out': False,
		'retail': Decimal(0),
		'scale_identifier': None,
		'special_cost': Decimal(0),
		'stock': False,
		#'to_be_announced': False,
	}
	
	latest_supplier_catalog_cache = dict()

	category_conversion_filter = None
	manufacturer_conversion_filter = None
	price_control_filter = None
	scale_conversion_filter = None

	def __init__(self):
		BaseSupplierCatalogTask.__init__(self)
		self.plugins = self.load_plugins()

	def load(self):
		"""Load"""
		logger.debug("Begin load()")
		self.load_all()
		logger.debug("End load()")

	def load_all(self, supplier_id=None):
		logger.debug("Begin load_all()")
		self.ts = ttystatus.TerminalStatus(period=1)
		self.ts.add(ttystatus.Literal('SupplierCatalogItem Load  Elapsed: '))
		self.ts.add(ttystatus.ElapsedTime())
		self.ts.add(ttystatus.Literal('  Supplier: '))
		self.ts.add(ttystatus.PercentDone('supplier_done', 'supplier_total', decimals=2))
		self.ts.add(ttystatus.Literal('  Manufacturer: '))
		self.ts.add(ttystatus.PercentDone('manufacturer_done', 'manufacturer_total', decimals=2))
		self.ts.add(ttystatus.Literal('  Product: '))
		self.ts.add(ttystatus.PercentDone('product_done', 'product_total', decimals=2))
		self.ts.add(ttystatus.Literal('  '))
		self.ts.add(ttystatus.String('manufacturer'))
		self.ts.add(ttystatus.Literal('-'))
		self.ts.add(ttystatus.String('product'))
		
		self.ts['supplier_total'] = 1
		self.ts['supplier_done'] = 0
		self.ts['manufacturer_total'] = 1
		self.ts['manufacturer_done'] = 0
		self.ts['product_total'] = 1
		self.ts['product_done'] = 0

		
		self.ts['supplier_total'] = len(self.plugins)
		self.ts['supplier_done'] = 0
		
		filter_supplier_id = supplier_id
		try:
			#self.session.begin(subtransactions=True)
			for plug in self.plugins.itervalues():
				supplier_id = plug.supplier_id()
				if (
					filter_supplier_id is not None and 
					supplier_id != filter_supplier_id
				):
					continue
				#latest_supplier_catalog = self.load_latest_supplier_catalog(supplier_id)
				#if supplier_catalog is not None:
					#self.supplier_catalog_id = supplier_catalog.id
				self.load_supplier(plug, supplier_id)
				#else:
					#logger.error("No Latest SupplierCatalog Found for Supplier.id %s", supplier_id)
				self.session.flush()
				self.session.expunge_all()
				
				self.ts['supplier_done'] += 1
			#self.session.commit()
		except Exception:
			logger.exception("Caught Exception: ")
			if self.session.transaction is not None:
				self.session.rollback()
		finally:
			self.ts.finish()
		logger.debug("End load_all()")


	def load_supplier(self, plug, supplier_id):
		self.session.begin(subtransactions=True)
		logger.debug("load_supplier %s", supplier_id)
		query = self.session.query(SupplierCatalogItemFieldModel.manufacturer_identifier)
		query = query.filter(SupplierCatalogItemFieldModel.supplier_id == supplier_id)
		query = query.filter(SupplierCatalogItemFieldModel.manufacturer_identifier != None)
		query = query.group_by(SupplierCatalogItemFieldModel.manufacturer_identifier)
		self.ts['manufacturer_total'] = query.count()
		self.ts['manufacturer_done'] = 0
		
		
		for (manufacturer_identifier, ) in query.yield_per(1000):
			self.ts['manufacturer'] = manufacturer_identifier
			self.load_manufacturer(plug, supplier_id, manufacturer_identifier)
			self.session.flush()
			self.session.expunge_all()
			self.ts['manufacturer_done'] += 1
		self.session.commit()

	def load_manufacturer(self, plug, supplier_id, manufacturer_identifier):
		logger.debug("Manufacturer %s", manufacturer_identifier)
		query = self.session.query(SupplierCatalogItemFieldModel.product_identifier)
		query = query.filter(SupplierCatalogItemFieldModel.supplier_id == supplier_id)
		query = query.filter(SupplierCatalogItemFieldModel.manufacturer_identifier == manufacturer_identifier)
		query = query.filter(SupplierCatalogItemFieldModel.product_identifier != None)

		query = query.group_by(SupplierCatalogItemFieldModel.product_identifier)
		self.ts['product_total'] = query.count()
		self.ts['product_done'] = 0
		
		for (product_identifier, ) in query.yield_per(1000):
			self.ts['product'] = product_identifier
			self.load_one(supplier_id, manufacturer_identifier, product_identifier)
			self.ts['product_done'] += 1

			
	def load_one(self, supplier_id, manufacturer_identifier, product_identifier):
		
		#for (key, value) in self.defaults.iteritems():
			#if key not in data or data[key] is None:
				#data[key] = value

		query = self.session.query(SupplierCatalogItemModel)
		query = query.filter(SupplierCatalogItemModel.supplier_id == supplier_id)
		query = query.filter(SupplierCatalogItemModel.manufacturer_identifier == manufacturer_identifier)
		query = query.filter(SupplierCatalogItemModel.product_identifier == product_identifier)
		
		try:
			supplier_catalog_item = query.one()
		except NoResultFound:
			supplier_catalog_item = SupplierCatalogItemModel()
			supplier_catalog_item.supplier_id = supplier_id
			supplier_catalog_item.manufacturer_identifier = manufacturer_identifier
			supplier_catalog_item.product_identifier = product_identifier
			self.session.add(supplier_catalog_item)
		
		#for (field_name, item_name) in self.field_names.iteritems():
			#setattr(supplier_catalog_item, item_name, data[field_name])
		#supplier_catalog_item.effective = data['effective']
		self.session.flush()


	def update(self):
		"""Update"""
		logger.debug("Begin update()")
		self.update_all(limit=10000, time_limit=timedelta(hours=1))
		logger.debug("End update()")


	def update_all(self, modified_since=None, limit=None, time_limit=None):
		"""Update All"""
		logger.debug("Begin update_all()")
		result = None
		ts = self.term_stat('SupplierCatalogItem Update')
		start_time = datetime.now()
		try:
			s = ScalableBloomFilter()
			query = self.session.query(
				SupplierCatalogItemFieldModel.supplier_id,
				SupplierCatalogItemFieldModel.manufacturer_identifier,
				SupplierCatalogItemFieldModel.product_identifier,
			)
			for row in query.yield_per(1000):
				s.add(row)
			
			query = self.session.query(SupplierCatalogItemModel)

			if modified_since:
				query = query.filter(SupplierCatalogItemModel.modified >= modified_since)
			if limit:
				query = query.order_by(SupplierCatalogItemModel.updated)
				query = query.limit(limit)

			ts['total'] = query.count()
			self.session.begin(subtransactions=True)
			for supplier_catalog_item in query.yield_per(10000):
				row = (
					supplier_catalog_item.supplier_id,
					supplier_catalog_item.manufacturer_identifier,
					supplier_catalog_item.product_identifier,
				)
				if row not in s:
					logger.info(
						"Not found in SupplierCatalogItemFields %s %s-%s", 
						supplier_catalog_item.supplier_id,
						supplier_catalog_item.manufacturer_identifier,
						supplier_catalog_item.product_identifier
					)
					## TODO Maybe only not do load from SCIV?
					continue

				self.update_one(supplier_catalog_item)
				ts['done'] += 1
				if time_limit is not None:
					if datetime.now() > start_time + time_limit:
						logger.info("Reached Time Limit at %i of %i", ts['done'], ts['total'])
						break;
			self.session.commit()
			result = True
		except Exception as e:
			logger.exception("Caught Exception: ")
			if self.session.transaction is not None:
				self.session.rollback()
		finally:
			ts.finish()
		logger.debug("End update_all()")
		return result
			
	def update_one(self, supplier_catalog_item):
		"""
		Update One
		
		Using ManufacturerConversion,
			convert manufacturer_identifier to manufacturer_id
		Using ProductConversion, 
			convert product_identifier to product_id and quantity
			quantity_cost from quantity, cost
			quantity_retail from quantity, retail
		Using CategoryConversion, 
			convert category_identifier to category_id
		Using ScaleConversion, 
			convert scale_identifier to scale_id
		Using PriceControl,
			get price_control_id
			using sale, quantity generate quantity_sale
		"""
		self.session.begin(subtransactions=True)
		
		self.update_supplier_catalog_item_version(supplier_catalog_item)
		
		self.update_manufacturer(supplier_catalog_item)
		self.update_product(supplier_catalog_item)
		self.update_category(supplier_catalog_item)
		self.update_scale(supplier_catalog_item)
		self.update_price_control(supplier_catalog_item)
		supplier_catalog_item.updated = datetime.now()
		self.session.commit()

	def load_latest_supplier_catalog(self, supplier_id):
		if supplier_id in self.latest_supplier_catalog_cache:
			return self.latest_supplier_catalog_cache[supplier_id]
		query = self.session.query(SupplierCatalogModel)
		query = query.filter(SupplierCatalogModel.supplier_id == supplier_id)
		supplier_catalog = query.order_by(desc(SupplierCatalogModel.issue_date)).first()
		logger.debug("Latest Supplier %s, %s", supplier_id, supplier_catalog)
		self.latest_supplier_catalog_cache[supplier_id] = supplier_catalog
		return supplier_catalog

	def update_supplier_catalog_item_version(self, supplier_catalog_item):
		if supplier_catalog_item.supplier_id not in self.plugins:
			## Not an ETL tracked Supplier.
			return
		
		plug = self.plugins[supplier_catalog_item.supplier_id]
		model_name = plug.version_model()  + 'Model'
		VersionModel = getattr(model, model_name)

		## TODO: Don't overwrite manual entries
		
		self.latest_supplier_catalog = self.load_latest_supplier_catalog(supplier_catalog_item.supplier_id)
		if self.latest_supplier_catalog is None:
			logger.error("No Latest SupplierCatalog Found for Supplier.id %s", supplier_catalog_item.supplier_id)
			## TODO: What should we be doing here? setting some sort of defaults?
			return

		query = self.session.query(SupplierCatalogItemFieldModel.id)
		query = query.filter(SupplierCatalogItemFieldModel.supplier_id == supplier_catalog_item.supplier_id)
		query = query.filter(SupplierCatalogItemFieldModel.manufacturer_identifier == supplier_catalog_item.manufacturer_identifier)
		query = query.filter(SupplierCatalogItemFieldModel.product_identifier == supplier_catalog_item.product_identifier)
	
		s = set()
		for (supplier_catalog_item_field_id, ) in query.yield_per(1000):
			s.add(supplier_catalog_item_field_id)

		del query

		if plug.opaque() is True:
			if plug.ghost() is True:
				data = self.coalesce_opaque_ghost(VersionModel, s, plug)
			else:
				data = self.coalesce_opaque_noghost(VersionModel, s)
		else:
			if plug.ghost() is True:
				data = self.coalesce_translucent_ghost(VersionModel, s)
			else:
				data = self.coalesce_translucent_noghost(VersionModel, s)
		#print "DATA IN", data
		
		if data is None:
			logger.warning(
				"Got None from coalesce %s %s-%s", 
				supplier_catalog_item.supplier_id,
				supplier_catalog_item.manufacturer_identifier,
				supplier_catalog_item.product_identifier,
			)
			## TODO What should we do here?
			return
		
		for (key, value) in self.defaults.iteritems():
			if key not in data or data[key] is None:
				data[key] = value

		#print "DATA OUT", data

		f = {
			'advanced':'advanced',
			#'availability_indefinite':'availability_indefinite',
			'available':'available',
			'category_identifier':'category_identifier',
			'cost':'quantity_cost',
			#'effective':'effective',
			##'manufacturer_identifier':'manufacturer_identifier', 
			'name':'name',
			'phased_out':'phased_out',
			##'product_identifier':'product_identifier',
			'retail':'quantity_retail', 
			'scale_identifier':'scale_identifier',
			'special_cost':'quantity_special_cost',
			'stock':'in_stock',
			#'to_be_announced':'to_be_announced'
		}

		for (field_name, item_name) in f.iteritems():
			setattr(supplier_catalog_item, item_name, data[field_name])


	def coalesce_opaque_noghost(self, VersionModel, s, get_effective=False):
		query = self.session.query(VersionModel)
		query = query.filter(VersionModel.supplier_catalog_item_field_id.in_(s))
		query = query.order_by(desc(VersionModel.effective))
		try:
			supplier_catalog_item_version = query.first()
		except NoResultFound:
			logger.debug('No %s Found', VersionModel.__name__)
			return None
		if supplier_catalog_item_version is None:
			logger.debug('No %s Found', VersionModel.__name__)
			return None
		data = dict()
		for field_name in self.field_names.iterkeys():
			data[field_name] = getattr(supplier_catalog_item_version.supplier_catalog_item_field, field_name)
		data['supplier_catalog_id'] = supplier_catalog_item_version.supplier_catalog_id
		
		supplier_catalog_item_field_id = supplier_catalog_item_version.supplier_catalog_item_field_id
		effective = supplier_catalog_item_version.effective
		
		if get_effective:
			for supplier_catalog_item_version in query.yield_per(5):
				if supplier_catalog_item_version.supplier_catalog_item_field_id == supplier_catalog_item_field_id:
					effective = supplier_catalog_item_version.effective
				else:
					break
			data['effective'] = effective
		return data


	def coalesce_opaque_ghost(self, VersionModel, s, plug, get_effective=False):
		data = self.coalesce_opaque_noghost(VersionModel, s, get_effective)
		if data is None: 
			return None
		
		if data['supplier_catalog_id'] != self.latest_supplier_catalog.id:
			if plug.ghost_stock():
				data['stock'] = False
			if plug.ghost_phased_out():
				data['phased_out'] = False
			if plug.ghost_advanced():
				data['advanced'] = False
		return data


	def coalesce_translucent_noghost(self, VersionModel, s):
		query = self.session.query(VersionModel)
		query = query.filter(VersionModel.supplier_catalog_item_field_id.in_(s))
		query = query.order_by(desc(VersionModel.effective))

		count = query.count()

		if count == 0:
			logger.error('No %s Found. Run SupplierCatalogItemVersionTask.vacuum() !', VersionModel.__name__)
			return None

		data = dict()
		first = True
		done = 0
		for supplier_catalog_item_version in query.all():
			done += 1
			if first:
				data['supplier_catalog_id'] = supplier_catalog_item_version.supplier_catalog_id
				data['effective'] = supplier_catalog_item_version.effective
			complete = True
			for field_name in self.field_names.iterkeys():
				field = getattr(supplier_catalog_item_version.supplier_catalog_item_field, field_name)
				if not field_name in data or data[field_name] is None:
					if field is None:
						complete = False
					else:
						data[field_name] = field
			if complete:
				break
		
		#logger.info("Complete SupplierCatalogItem was found in %i of %i Versions", done, count)
				
		return data

	def coalesce_translucent_ghost(self, VersionModel, s, plug):
		data = self.coalesce_translucent_noghost(VersionModel, s)
		if data is None: 
			return None
		
		if data['supplier_catalog_id'] != self.latest_supplier_catalog.id:
			if plug.ghost_stock():
				data['stock'] = False
			if plug.ghost_phased_out():
				data['phased_out'] = False
			if plug.ghost_advanced():
				data['advanced'] = False
		return data


	def update_manufacturer(self, supplier_catalog_item):
		#self.session.begin(subtransactions=True)
		"""Update Manufacturer"""
		#print (
		#	"Update Manufacturer", 
		#	"sid", supplier_catalog_item.supplier_id, 
		#	"mident", supplier_catalog_item.manufacturer_identifier,
		#	"mid", supplier_catalog_item.manufacturer_id
		#)

		manufacturer_conversion = self.get_manufacturer_conversion(
			supplier_catalog_item.supplier_id, 
			supplier_catalog_item.manufacturer_identifier
		)
		if manufacturer_conversion is not None:
			supplier_catalog_item.manufacturer_id = manufacturer_conversion.manufacturer_id
		else:
			supplier_catalog_item.manufacturer_id = None
		#self.session.commit()


	def update_product(self, supplier_catalog_item):
		#self.session.begin(subtransactions=True)
		"""Product Conversion"""
		if (
			supplier_catalog_item.supplier_id is not None and
			supplier_catalog_item.manufacturer_id is not None and
			supplier_catalog_item.product_identifier is not None
		):
			product_conversion = self.get_product_conversion(
				supplier_catalog_item.supplier_id, 
				supplier_catalog_item.manufacturer_id,
				supplier_catalog_item.product_identifier
			)
			if product_conversion is not None:
				supplier_catalog_item.product_id = product_conversion.product_id
				supplier_catalog_item.quantity = product_conversion.get_quantity()
			else:
				supplier_catalog_item.product_id = None
				supplier_catalog_item.quantity = Decimal(1)
		else:
			supplier_catalog_item.product_id = None
			supplier_catalog_item.quantity = Decimal(1)

		if supplier_catalog_item.quantity_cost > 0:
			supplier_catalog_item.cost = decimal_round(supplier_catalog_item.quantity_cost / supplier_catalog_item.quantity, cfg.cost_decimals)
		else:
			supplier_catalog_item.cost = Decimal(0)
			
		if supplier_catalog_item.quantity_special_cost > 0:
			supplier_catalog_item.special_cost = decimal_round(supplier_catalog_item.quantity_special_cost / supplier_catalog_item.quantity, cfg.cost_decimals)
		else:
			supplier_catalog_item.special_cost = Decimal(0)
			
		if supplier_catalog_item.quantity_retail > 0:
			supplier_catalog_item.retail = decimal_round(supplier_catalog_item.quantity_retail / supplier_catalog_item.quantity, cfg.cost_decimals)
		else:
			supplier_catalog_item.retail = Decimal(0)
		#self.session.commit()

	def update_category(self, supplier_catalog_item):
		"""Category Conversion"""
		#self.session.begin(subtransactions=True)
		if (
			supplier_catalog_item.supplier_id is not None and
			supplier_catalog_item.manufacturer_id is not None and
			supplier_catalog_item.category_identifier is not None
		):
			category_conversion = self.get_category_conversion(
				supplier_catalog_item.supplier_id, 
				supplier_catalog_item.manufacturer_id, 
				supplier_catalog_item.category_identifier
			)
			if category_conversion is not None:
				supplier_catalog_item.category_id = category_conversion.category_id
			else:
				supplier_catalog_item.category_id = None
		else:
			supplier_catalog_item.category_id = None
		#self.session.commit()


	def update_scale(self, supplier_catalog_item):
		"""Scale Conversion"""
		#self.session.begin(subtransactions=True)
		if (
			supplier_catalog_item.supplier_id is not None and
			supplier_catalog_item.scale_identifier is not None
		):
			scale_conversion = self.get_scale_conversion(
				supplier_catalog_item.supplier_id, 
				supplier_catalog_item.scale_identifier
			)
			if scale_conversion is not None:
				supplier_catalog_item.scale_id = scale_conversion.scale_id
			else:
				supplier_catalog_item.scale_id = None
		else:
			supplier_catalog_item.scale_id = None
		#self.session.commit()


	def update_price_control(self, supplier_catalog_item):
		"""Price Control"""
		#self.session.begin(subtransactions=True)
		#*** TODO handle price_control.allow_advanced
		
		if (
			supplier_catalog_item.supplier_id is not None and
			supplier_catalog_item.manufacturer_id is not None and
			supplier_catalog_item.retail > 0
		):
			price_control = self.get_price_control(
				supplier_catalog_item.supplier_id, 
				supplier_catalog_item.manufacturer_id, 
				supplier_catalog_item.retail, 
				supplier_catalog_item.advanced, 
				supplier_catalog_item.special
			)
			if price_control is not None:
				supplier_catalog_item.price_control_id = price_control.id
				supplier_catalog_item.rank = price_control.rank
				if supplier_catalog_item.special:
					if supplier_catalog_item.cost > 0:
						ratio = supplier_catalog_item.special_cost / supplier_catalog_item.cost
					else:
						ratio = 1
					special_retail = supplier_catalog_item.retail * ratio
					supplier_catalog_item.sale = price_control.sale(
						supplier_catalog_item.special_cost,
						special_retail
					)
				else:
					supplier_catalog_item.sale = price_control.sale(
						supplier_catalog_item.cost,
						supplier_catalog_item.retail
					)
			else:
				supplier_catalog_item.sale = 0
				supplier_catalog_item.price_control_id = None
				supplier_catalog_item.rank = 0
		else:
			supplier_catalog_item.sale = 0
			supplier_catalog_item.price_control_id = None
			supplier_catalog_item.rank = 0
		#self.session.commit()


	def get_category_conversion(self, supplier_id, manufacturer_id, category_identifier):
		"""Category Conversion"""
		if self.category_conversion_filter is None:
			self.category_conversion_filter = ScalableBloomFilter()
			query = self.session.query(
				CategoryConversionModel.supplier_id,
				CategoryConversionModel.manufacturer_id,
				CategoryConversionModel.needle
			)
			for row in query.yield_per(100):
				self.category_conversion_filter.add(row)
		
		row = (supplier_id, manufacturer_id, category_identifier)
		if row in self.category_conversion_filter:
			query = self.session.query(CategoryConversionModel)
			query = query.filter(CategoryConversionModel.supplier_id == supplier_id)
			query = query.filter(CategoryConversionModel.manufacturer_id == manufacturer_id)
			query = query.filter(CategoryConversionModel.needle == category_identifier)
			try:
				category_conversion = query.one()
				return category_conversion
			except NoResultFound:
				pass

		category_conversion = CategoryConversionModel()
		category_conversion.manufacturer_id = manufacturer_id
		category_conversion.supplier_id = supplier_id
		category_conversion.needle = category_identifier
		self.session.add(category_conversion)
		self.category_conversion_filter.add(row)
		return category_conversion
		
		
	def get_manufacturer_conversion(self, supplier_id, manufacturer_identifier):
		"""Manufacturer Conversion"""
		if self.manufacturer_conversion_filter is None:
			self.manufacturer_conversion_filter = ScalableBloomFilter()
			query = self.session.query(
				ManufacturerConversionModel.supplier_id,
				ManufacturerConversionModel.manufacturer_identifier
			)
			for row in query.yield_per(100):
				self.manufacturer_conversion_filter.add(row)
		
		row = (supplier_id, manufacturer_identifier)
		if row in self.manufacturer_conversion_filter:
			query = self.session.query(ManufacturerConversionModel)
			query = query.filter(ManufacturerConversionModel.supplier_id == supplier_id)
			query = query.filter(ManufacturerConversionModel.manufacturer_identifier == manufacturer_identifier)
			try:
				manufacturer_conversion = query.one()
				return manufacturer_conversion
			except NoResultFound:
				pass
			
		query = self.session.query(ManufacturerModel)
		query = query.filter(ManufacturerModel.identifier == manufacturer_identifier)
		try:
			manufacturer = query.one()
		except NoResultFound:
			logger.warning("No ManufacturerConversion found for supplier_id '%s' manufacturer_identifier '%s'", supplier_id, manufacturer_identifier)
			return None
		
		manufacturer_conversion = ManufacturerConversionModel()
		manufacturer_conversion.manufacturer_id = manufacturer.id
		manufacturer_conversion.supplier_id = supplier_id
		manufacturer_conversion.manufacturer_identifier = manufacturer_identifier
		#self.session.add(manufacturer_conversion)
		return manufacturer_conversion


	def get_price_control(self, supplier_id, manufacturer_id, retail, preorder, special):
		"""Price Control"""
		if self.price_control_filter is None:
			self.price_control_filter = ScalableBloomFilter()
			query = self.session.query(
				PriceControlModel.supplier_id,
				PriceControlModel.manufacturer_id
			)
			for row in query.yield_per(100):
				self.price_control_filter.add(row)
		
		row = (supplier_id, manufacturer_id)
		if row in self.price_control_filter:
			query = self.session.query(PriceControlModel)
			query = query.filter(PriceControlModel.supplier_id == supplier_id)
			query = query.filter(PriceControlModel.manufacturer_id == manufacturer_id)
			if preorder:
				query = query.filter(PriceControlModel.preorder == True)
				
			if special:
				query = query.filter(PriceControlModel.special == True)
			
			if (not preorder) and (not special):
				query = query.filter(PriceControlModel.normal == True)
			
			query = query.filter(PriceControlModel.retail_low <= retail)
			query = query.filter(PriceControlModel.retail_high >= retail)
			query = query.filter(PriceControlModel.enable == True)
			try:
				price_control = query.one()
				return price_control
			except NoResultFound:
				#logger.warning(
				#	"No PriceControl found for supplier_id '%s' manufacturer_id '%s' retail '%s', preorder '%s', special '%s'", 
				#	supplier_id, 
				#	manufacturer_id, 
				#	retail, 
				#	preorder, 
				#	special
				#)
				return None
			except MultipleResultsFound:
				logger.warning(
					"Duplicate PriceControls found for supplier_id '%s' manufacturer_id '%s' retail '%s', preorder '%s', special '%s'", 
					supplier_id, 
					manufacturer_id, 
					retail, 
					preorder, 
					special
				)
		return None


	def get_product_conversion(self, supplier_id, manufacturer_id, product_identifier):
		"""Product Conversion"""
		query = self.session.query(ProductConversionModel)
		query = query.filter(ProductConversionModel.supplier_id == supplier_id)
		query = query.filter(ProductConversionModel.manufacturer_id == manufacturer_id)
		query = query.filter(ProductConversionModel.product_identifier == product_identifier)
		
		try:
			product_conversion = query.one()
			return product_conversion
		except NoResultFound:
			pass
			
		query = self.session.query(ProductModel)
		query = query.filter(ProductModel.manufacturer_id == manufacturer_id)
		query = query.filter(ProductModel.identifier == product_identifier)

		try:
			product = query.one()
		except NoResultFound:
			#logger.warning(
			#	"No ProductConversion found for supplier_id '%s' manufacturer_id '%s' product_identifier '%s'", 
			#	supplier_id, 
			#	manufacturer_id, 
			#	product_identifier, 
			#)
			return None
			
		product_conversion = ProductConversionModel()
		product_conversion.product_id = product.id
		product_conversion.manufacturer_id = manufacturer_id
		product_conversion.supplier_id = supplier_id
		product_conversion.source_quantity = 1
		product_conversion.target_quantity = 1
		return product_conversion


	def get_scale_conversion(self, supplier_id, scale_identifier):
		"""Scale Conversion"""
		
		if scale_identifier is None:
			return None
		if supplier_id is None:
			return None


		if self.scale_conversion_filter is None:
			self.scale_conversion_filter = ScalableBloomFilter()
			query = self.session.query(
				ScaleConversionModel.supplier_id,
				ScaleConversionModel.scale_identifier
			)
			for row in query.yield_per(100):
				self.scale_conversion_filter.add(row)
		
		row = (supplier_id, scale_identifier)
		if row in self.scale_conversion_filter:
			
			query = self.session.query(ScaleConversionModel)
			query = query.filter(ScaleConversionModel.supplier_id == supplier_id)
			query = query.filter(ScaleConversionModel.scale_identifier == scale_identifier)
			
			try:
				scale_conversion = query.one()
				return scale_conversion
			except NoResultFound:
				pass

		query = self.session.query(ScaleModel)
		query = query.filter(ScaleModel.name == scale_identifier)

		try:
			scale = query.one()
		except NoResultFound:
			scale = None

		if scale is not None:
			scale_conversion = ScaleConversionModel()
			scale_conversion.scale_id = scale.id
			return scale_conversion
		else:
			scale_conversion = ScaleConversionModel()
			scale_conversion.scale_id = None
			scale_conversion.supplier_id = supplier_id
			scale_conversion.scale_identifier = scale_identifier
			self.session.add(scale_conversion)
			self.scale_conversion_filter.add(row)
			self.session.flush()
			return scale_conversion
