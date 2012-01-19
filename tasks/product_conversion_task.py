#!/usr/bin/python
#from engine import enginemaker
#from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

#from sql_mapping import CategoryConversion
#from sql_mapping import Manufacturer, ManufacturerConversion
from sql_mapping import ProductConversion
#from sql_mapping import ScaleConversion
from sql_mapping import SupplierCatalogItem

#from caching_query import FromCache

#from environment import Session
from session import Session

from progressbar import Bar, Percentage, ETA, FileTransferSpeed, ProgressBar

import uuid

class ProductConversionTask(object):
	
	def __init__(self):
		"""Init"""
		self.session = Session(autocommit=True)
	
	
	def load_all_supplier_catalog_items(self):
		"""Load All SupplierCatalogItems"""
		
		query = self.session.query(SupplierCatalogItem)

		count = query.count()
		i = 0;

		pbar = ProgressBar(widgets=[Percentage(), FileTransferSpeed(), Bar()], maxval=count).start()

		for supplier_catalog_item in query.yield_per(1000):
			self.session.begin()
			self.load_one_supplier_catalog_item(supplier_catalog_item)
			self.session.commit()
			pbar.update(i)
			i+=1
		


	def load_one_supplier_catalog_item(self, supplier_catalog_item):
		
		pass

		
if __name__ == '__main__':
	product_conversion_task = ProductConversionTask()
	product_conversion_task.load_all_supplier_catalog_items()
