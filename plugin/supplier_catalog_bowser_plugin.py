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
#Standard Library
import logging 
import re
from datetime import datetime
#import uuid
#from decimal import *

#Extended Library
#from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
#import ttystatus

#Application Library
#from models import Supplier
#from models import SupplierCatalog
#from models import SupplierCatalogItem
#import cfg


#This Package
from plugin.base_plugin import BasePlugin

logger = logging.getLogger(__name__)

class SupplierCatalogBowserPlugin(BasePlugin):
	
	supplier_catalog_filter = None

	def __init__(self, supplier_catalog_filter):
		BasePlugin.__init__(self)
		self.supplier_catalog_filter = supplier_catalog_filter

	def match_file_import(self, file_import):
		if re.search('lock', file_import.name):
			return False
		if not re.search('DealerOutsideWebExport', file_import.name):
			return False
		if re.search('Bowser', file_import.content[:1000]):
			return True
		return False

	""" *** Getter Functions *** """
	def supplier_id(self):
		return self.supplier_catalog_filter.supplier_id

	def supplier_catalog_filter_id(self):
		return self.supplier_catalog_filter.id
		
	def issue_date(self, file_import):

		#5-09-2011 DealerOutsideWebExport
		#7-5-2011 Bowser DealerOutsideWebExport.txt
		m = re.search('(\d{1,2})-(\d{1,2})-(\d{4}) (Bowser ){0,1}DealerOutsideWebExport', file_import.name)
		if m:
			return datetime(int(m.group(3)), int(m.group(1)), int(m.group(2)))

		#11302011 DealerOutsideWebExport.txt
		m = re.search('(\d{2})(\d{2})(\d{4}) DealerOutsideWebExport', file_import.name)
		if m:
			return datetime(int(m.group(3)), int(m.group(1)), int(m.group(2)))

		logger.warning("Failed to convert issue_date for %s", file_import.name)
		return file_import.effective
