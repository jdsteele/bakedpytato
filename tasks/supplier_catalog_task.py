#Standard Library
import logging 
import uuid
from decimal import *

#Extended Library
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
import ttystatus

#Application Library
from models import Supplier
from models import SupplierCatalog
from models import SupplierCatalogItem
import cfg


#This Package
from tasks.base_task import BaseTask


logger = logging.getLogger(__name__)

class SupplierCatalogTask(BaseTask):

	def update_all(self):
		"""Update All"""
		logger.debug("Begin update_all()")
		self.sort()
		logger.debug("End update_all()")
		
	def sort(self):
		logger.debug("Begin sort()")
		query = self.session.query(Supplier)
		suppliers = query.all()
		
		for supplier in suppliers:
			#print supplier
			query = self.session.query(SupplierCatalog)
			query = query.filter(SupplierCatalog.supplier_id == supplier.id)
			query = query.order_by(SupplierCatalog.issue_date)
			
			prev_supplier_catalog = None
			
			for supplier_catalog in query:
				#print supplier_catalog
				if prev_supplier_catalog is not None:
					prev_supplier_catalog.next_supplier_catalog_id = supplier_catalog.id
					supplier_catalog.prev_supplier_catalog_id = prev_supplier_catalog.id
				prev_supplier_catalog = supplier_catalog
			supplier_catalog.next_supplier_catalog_id = None
		logger.debug("End sort()")
