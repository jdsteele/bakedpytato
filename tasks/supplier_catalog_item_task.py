#Standard Library
import logging 
import uuid
from decimal import *

#Extended Library
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import ttystatus

#Application Library
from models import CategoryConversion
from models import Manufacturer, ManufacturerConversion
from models import PriceControl
from models import Product, ProductConversion
from models import Scale, ScaleConversion
from models import SupplierCatalogItem
import cfg

#This Package
from tasks.base_task import BaseTask


logger = logging.getLogger(__name__)

class SupplierCatalogItemTask(BaseTask):
	
		


	def update_all(self):
		"""Update All"""
		logger.debug("Begin update_all()")
		query = self.session.query(SupplierCatalogItem)

		ts = ttystatus.TerminalStatus(period=0.5)
		ts.add(ttystatus.Literal('Updating Catalog Items '))
		ts.add(ttystatus.Literal(' Elapsed: '))
		ts.add(ttystatus.ElapsedTime())
		ts.add(ttystatus.Literal(' Remaining: '))
		ts.add(ttystatus.RemainingTime('done', 'total'))
		ts.add(ttystatus.Literal(' '))
		ts.add(ttystatus.PercentDone('done', 'total', decimals=2))
		ts.add(ttystatus.Literal(' '))
		ts.add(ttystatus.ProgressBar('done', 'total'))
		ts['total'] = query.count()
		ts['done'] = 0

		self.session.begin()
		for supplier_catalog_item in query.yield_per(1000):
			self.update_one(supplier_catalog_item)
			self.session.flush()
			ts['done'] += 1
		ts.clear()
		ts.add(ttystatus.Literal(' Committing '))
		ts.add(ttystatus.ElapsedTime())
		self.session.commit()
		ts.finish()
		logger.debug("End update_all()")
			
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
		
		
		
		self.update_manufacturer(supplier_catalog_item)
		self.update_product(supplier_catalog_item)
		self.update_category(supplier_catalog_item)
		self.update_scale(supplier_catalog_item)
		#supplier_catalog_item.set_debug(True)
		self.update_price_control(supplier_catalog_item)
		#supplier_catalog_item.set_debug(False)


	def update_manufacturer(self, supplier_catalog_item):
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


	def update_product(self, supplier_catalog_item):
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
			supplier_catalog_item.cost = PriceControl.round(supplier_catalog_item.quantity_cost / supplier_catalog_item.quantity, cfg.cost_decimals)
		else:
			supplier_catalog_item.cost = Decimal(0)
			
		if supplier_catalog_item.quantity_special_cost > 0:
			supplier_catalog_item.special_cost = PriceControl.round(supplier_catalog_item.quantity_special_cost / supplier_catalog_item.quantity, cfg.cost_decimals)
		else:
			supplier_catalog_item.special_cost = Decimal(0)
			
		if supplier_catalog_item.quantity_retail > 0:
			supplier_catalog_item.retail = PriceControl.round(supplier_catalog_item.quantity_retail / supplier_catalog_item.quantity, cfg.cost_decimals)
		else:
			supplier_catalog_item.retail = Decimal(0)

	def update_category(self, supplier_catalog_item):
		"""Category Conversion"""
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


	def update_scale(self, supplier_catalog_item):
		"""Scale Conversion"""
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


	def update_price_control(self, supplier_catalog_item):
		"""Price Control"""
		
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


	def get_category_conversion(self, supplier_id, manufacturer_id, category_identifier):
		"""Category Conversion"""
		query = self.session.query(CategoryConversion)	#.options(FromCache("default", "manufacturer_conversion"))
		query = query.filter(CategoryConversion.supplier_id == supplier_id)
		query = query.filter(CategoryConversion.manufacturer_id == manufacturer_id)
		query = query.filter(CategoryConversion.needle == category_identifier)
		try:
			category_conversion = query.one()
			return category_conversion
		except NoResultFound:
			pass
		category_conversion = CategoryConversion()
		category_conversion.manufacturer_id = manufacturer_id
		category_conversion.supplier_id = supplier_id
		category_conversion.needle = category_identifier
		self.session.add(category_conversion)
		return category_conversion
		
		
	def get_manufacturer_conversion(self, supplier_id, manufacturer_identifier):
		"""Manufacturer Conversion"""
		query = self.session.query(ManufacturerConversion)	#.options(FromCache("default", "manufacturer_conversion"))
		query = query.filter(ManufacturerConversion.supplier_id == supplier_id)
		query = query.filter(ManufacturerConversion.manufacturer_identifier == manufacturer_identifier)
		try:
			manufacturer_conversion = query.one()
			return manufacturer_conversion
		except NoResultFound:
			pass
			
		query = self.session.query(Manufacturer)	#.options(FromCache("default", "manufacturer_conversion"))
		query = query.filter(Manufacturer.identifier == manufacturer_identifier)
		try:
			manufacturer = query.one()
		except NoResultFound:
			logger.warning("No ManufacturerConversion found for supplier_id '%s' manufacturer_identifier '%s'", supplier_id, manufacturer_identifier)
			return None
		
		manufacturer_conversion = ManufacturerConversion()
		manufacturer_conversion.manufacturer_id = manufacturer.id
		#manufacturer_conversion.id = str(uuid.uuid4())
		manufacturer_conversion.supplier_id = supplier_id
		manufacturer_conversion.manufacturer_identifier = manufacturer_identifier
		#self.session.add(manufacturer_conversion)
		return manufacturer_conversion


	def get_price_control(self, supplier_id, manufacturer_id, retail, preorder, special):
		"""Price Control"""
		query = self.session.query(PriceControl)	#.options(FromCache("default", "manufacturer_conversion"))
		query = query.filter(PriceControl.supplier_id == supplier_id)
		query = query.filter(PriceControl.manufacturer_id == manufacturer_id)
		if preorder:
			query = query.filter(PriceControl.preorder == True)
			
		if special:
			query = query.filter(PriceControl.special == True)
		
		if (not preorder) and (not special):
			query = query.filter(PriceControl.normal == True)
		
		query = query.filter(PriceControl.retail_low <= retail)
		query = query.filter(PriceControl.retail_high >= retail)
		query = query.filter(PriceControl.enable == True)
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
		query = self.session.query(ProductConversion)	#.options(FromCache("default", "product_conversion"))
		query = query.filter(ProductConversion.supplier_id == supplier_id)
		query = query.filter(ProductConversion.manufacturer_id == manufacturer_id)
		query = query.filter(ProductConversion.product_identifier == product_identifier)
		
		try:
			product_conversion = query.one()
			return product_conversion
		except NoResultFound:
			pass
			
		query = self.session.query(Product)
		query = query.filter(Product.manufacturer_id == manufacturer_id)
		query = query.filter(Product.identifier == product_identifier)

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
			
		product_conversion = ProductConversion()
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
		
		query = self.session.query(ScaleConversion)	#.options(FromCache("default", "product_conversion"))
		query = query.filter(ScaleConversion.supplier_id == supplier_id)
		query = query.filter(ScaleConversion.scale_identifier == scale_identifier)
		
		try:
			scale_conversion = query.one()
			return scale_conversion
		except NoResultFound:
			pass

		query = self.session.query(Scale)
		query = query.filter(Scale.name == scale_identifier)

		try:
			scale = query.one()
		except NoResultFound:
			scale = None

		if scale is not None:
			scale_conversion = ScaleConversion()
			scale_conversion.scale_id = scale.id
			return scale_conversion
		else:
			scale_conversion = ScaleConversion()
			scale_conversion.scale_id = None
			scale_conversion.supplier_id = supplier_id
			scale_conversion.scale_identifier = scale_identifier
			self.session.add(scale_conversion)
			self.session.flush()
			return scale_conversion
