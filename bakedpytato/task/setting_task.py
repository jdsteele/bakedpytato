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
import logging 
#import uuid
#from decimal import *

#Extended Library
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

#Application Library
from bakedpytato import cfg
#from model import CategoryConversionModel
#from model import ManufacturerModel, ManufacturerConversionModel
#from model import PriceControlModel
#from model import ProductModel, ProductConversionModel
#from model import ScaleModel, ScaleConversionModel
from bakedpytato.model import SettingModel

#This Package
#import priceutil
from bakedpytato.task.base_task import BaseTask

logger = logging.getLogger(__name__)

class SettingTask(BaseTask):
	
	def get(self, class_name, name, default=None):
		self.session.begin(subtransactions=True)
		query = self.session.query(SettingModel)
		query = query.filter(SettingModel.class_ == class_name)
		query = query.filter(SettingModel.name == name)
		try:
			setting = query.one()
		except NoResultFound:
			setting = None
		
		self.session.commit()
		if setting:
			return setting.value
		return default
		
	def set(self, class_name, name, value):
		self.session.begin(subtransactions=True)
		query = self.session.query(SettingModel)
		query = query.filter(SettingModel.class_ == class_name)
		query = query.filter(SettingModel.name == name)
		try:
			setting = query.one()
		except NoResultFound:
			setting = SettingModel()
			setting.class_ = class_name
			setting.name = name
			self.session.add(setting)
		
		setting.value = value
		self.session.commit()
