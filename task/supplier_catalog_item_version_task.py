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

#Extended Library
from sqlalchemy.orm.exc import NoResultFound

#Application Library
from model import SupplierCatalogModel
from model import SupplierCatalogItemVersionModel

#This Package
from task.base_task import BaseTask

logger = logging.getLogger(__name__)

class SupplierCatalogItemVersionTask(BaseTask):
	
	def update_all(self):
		logger.debug("Begin update_all()")
		query = self.session.query(SupplierCatalogModel)

		ts = self.term_stat("Updating SCIV From SC", query.count())
		for supplier_catalog in query:
			self.update_from_supplier_catalog(supplier_catalog)
			ts['done'] += 1
		ts.finish()
		logger.debug("End update_all()")
	
	def update_from_supplier_catalog(self, supplier_catalog):
		query = self.session.query(SupplierCatalogItemVersionModel)
		query = query.filter(SupplierCatalogItemVersionModel.supplier_catalog_id == supplier_catalog.id)

		values = dict()
		values['prev_supplier_catalog_id'] = supplier_catalog.prev_supplier_catalog_id
		values['next_supplier_catalog_id'] = supplier_catalog.next_supplier_catalog_id
		values['effective'] = supplier_catalog.issue_date
		query.update(values, synchronize_session=False)
