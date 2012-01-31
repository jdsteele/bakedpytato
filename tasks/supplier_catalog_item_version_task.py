#Standard Library
import logging 

#Extended Library
from sqlalchemy.orm.exc import NoResultFound

#Application Library
from models import SupplierCatalog
from models import SupplierCatalogItemVersion

#This Package
from tasks.base_task import BaseTask

logger = logging.getLogger(__name__)

class SupplierCatalogItemVersionTask(BaseTask):
	
	def update_all(self):
		logger.debug("Begin update_all()")
		query = self.session.query(SupplierCatalog)

		ts = self.term_stat("Updating SCIV From SC", query.count())
		for supplier_catalog in query:
			self.update_supplier_catalog(supplier_catalog)
			ts['done'] += 1
		ts.finish()
		logger.debug("End update_all()")
	
	def update_supplier_catalog(self, supplier_catalog):
		query = self.session.query(SupplierCatalogItemVersion)
		query = query.filter(SupplierCatalogItemVersion.supplier_catalog_id == supplier_catalog.id)

		values = dict()
		values['prev_supplier_catalog_id'] = supplier_catalog.prev_supplier_catalog_id
		values['next_supplier_catalog_id'] = supplier_catalog.next_supplier_catalog_id
		values['effective'] = supplier_catalog.issue_date
		query.update(values, synchronize_session=False)


	def junk(self):
		for supplier_catalog_item_version in query.yield_per(10000):
			
			#print i, '/', count, "\r",
			
			pbar.update(i)
			i+=1
			
			#session.begin()
			#session.add(supplier_catalog_item_version)
			
			#*** Supplier Catalog ***
			query2 = session2.query(SupplierCatalog).options(FromCache("default", "supplier_catalog"))
			query2 = query2.filter(SupplierCatalog.id == supplier_catalog_item_version.supplier_catalog_id)

			try:
				supplier_catalog = query2.one()
				supplier_catalog_item_version.next_supplier_catalog_id = supplier_catalog.next_supplier_catalog_id
			except NoResultFound:
				supplier_catalog_item_version.next_supplier_catalog_id = None
			#if supplier_catalog_item_version.is_dirty():
			if i % 100 == 0:
				session.flush()
				session2.flush()
			if i % 100000 == 0:
				print "\n", time.strftime('%Y-%m-%d %H:%M:%S %Z'), "\n"

		print "\n", "Commiting", time.strftime('%Y-%m-%d %H:%M:%S %Z'), "\n"
		session.commit()
		print "\n", "Comitted", time.strftime('%Y-%m-%d %H:%M:%S %Z'), "\n"
