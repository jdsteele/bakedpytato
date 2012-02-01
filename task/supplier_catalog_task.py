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
import uuid
from decimal import *

#Extended Library
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import ttystatus

#Application Library
from model import SupplierModel
from model import SupplierCatalogModel
from model import SupplierCatalogItemModel
import cfg


#This Package
from task.base_task import BaseTask


logger = logging.getLogger(__name__)

class SupplierCatalogTask(BaseTask):

	def update_all(self):
		"""Update All"""
		logger.debug("Begin update_all()")
		self.sort()
		logger.debug("End update_all()")
		
	def sort(self):
		logger.debug("Begin sort()")
		query = self.session.query(SupplierModel)
		suppliers = query.all()
		
		for supplier in suppliers:
			#print supplier
			query = self.session.query(SupplierCatalogModel)
			query = query.filter(SupplierCatalogModel.supplier_id == supplier.id)
			query = query.order_by(SupplierCatalogModel.issue_date)
			
			prev_supplier_catalog = None
			
			for supplier_catalog in query:
				#print supplier_catalog
				if prev_supplier_catalog is not None:
					prev_supplier_catalog.next_supplier_catalog_id = supplier_catalog.id
					supplier_catalog.prev_supplier_catalog_id = prev_supplier_catalog.id
				prev_supplier_catalog = supplier_catalog
			supplier_catalog.next_supplier_catalog_id = None
		logger.debug("End sort()")
