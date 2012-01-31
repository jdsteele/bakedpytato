#Standard Library
import logging
import re
import uuid
from decimal import *

#Extended Library
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy import or_, desc
import ttystatus

#Application Library
import models

#This Package
from tasks.base_task import BaseTask

logger = logging.getLogger(__name__)

def get_model(model_name):
	g = globals()
	if model_name in g['models'].__dict__:
		return g['models'].__dict__[model_name]
	return None

def get_model_attribute(model_name, attribute_name):
	model = get_model(model_name)
	if model:
		return model.__dict__[attribute_name]
	return None

class BarcodeConversionTask(BaseTask):

	def __init__(self):
		BaseTask.__init__(self)
		#barcode_conversions cache
		query = self.session.query(models.BarcodeConversion)
		self.barcode_conversions = query.all()
		
		#barcode to object cache
		self.cache = dict()

	def get(self, barcode):
		
		if barcode in self.cache:
			return self.cache[barcode]
		
		self.cache[barcode] = None
		
		product_barcode = self.get_product_barcode(barcode)
		if product_barcode:
			product_id = product_barcode.product_id
			
			obj = self.session.query(models.Product).filter(Product.id == product_id).one()
			self.cache[barcode] = obj
			return self.cache[barcode]
			
		barcode_conversion = self.get_barcode_conversion(barcode)
		if barcode_conversion:
			obj = self.convert(barcode, barcode_conversion)
			self.cache[barcode] = obj
		
		return self.cache[barcode]
		
	def get_product_barcode(self, barcode):
		query = self.session.query(models.ProductBarcode)
		query = query.filter(models.ProductBarcode.barcode == barcode)
		if query.count() == 1:
			product_barcode = query.one()
			return product_barcode
		elif query.count() > 1:
			print "Found Too Many Matches for" . barcode
		return None

	def get_barcode_conversion(self, barcode):
		product_id = None
		for barcode_conversion in self.barcode_conversions:
			regex = barcode_conversion.regex.lstrip('/').rstrip('/')
			match = re.match(regex, barcode)
			if match:
				return barcode_conversion
		return None
				

	def convert(self, barcode, barcode_conversion):
		regex = barcode_conversion.regex.lstrip('/').rstrip('/')
		match = re.match(regex, barcode)
		MatchClass = get_model(barcode_conversion.match_class)
		if MatchClass:
			query = self.session.query(MatchClass)

			y = [barcode_conversion.match_1, barcode_conversion.match_2, barcode_conversion.match_3]
				
			for i in xrange(0,2):
				if y[i]:
					s = re.split('\.', y[i], 2)
					model_attribute = get_model_attribute(s[0], s[1])
					#print 'S:', s
					if model_attribute:
						g = match.group(i + 1).lstrip('0')
						#print 'CA:', class_attribute, '==', g
						query = query.filter(model_attribute == g)

			z = [
				[1, barcode_conversion.condition_1_name, barcode_conversion.condition_1_value],
				[2, barcode_conversion.condition_2_name, barcode_conversion.condition_2_value],
				[3, barcode_conversion.condition_3_name, barcode_conversion.condition_3_value]
			]
				
			for (i, condition_name, condition_value) in z:
					
				#print 'I:', i, condition_name, condition_value
					
				if condition_name:
					s = re.split('\.', condition_name, 2)
					#print 'SS:', s
					model_attribute = get_model_attribute(s[0], s[1])
					if model_attribute:
						#print 'CA:', class_attribute, '==', condition_value
						query = query.filter(model_attribute == condition_value)
						
			
			if query.count() == 1:
				matched = query.one()
				#print "matched", matched
				
				a = self.underscore(barcode_conversion.output_class) + '_id'
				match_id = matched.__dict__[a]
				#print "match_id", match_id

				if match_id is not None:
					OutputClass = get_model(barcode_conversion.output_class)
					#print 'OutputClass', OutputClass
					query = self.session.query(OutputClass)
					
					output_id_attrib = get_model_attribute(barcode_conversion.output_class, 'id')
					#print 'output_id_attrib', output_id_attrib, '==', id
					
					query = query.filter(output_id_attrib == match_id)
					return query.one()
		return None
