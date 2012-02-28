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
### Pragma
from __future__ import unicode_literals

### Standard Library
import logging 

### Extended Library
from sqlalchemy.orm.exc import NoResultFound

### Application Library
from bakedpytato import plugin
from bakedpytato.model import metadata, DBSession
from bakedpytato.model import SupplierCatalogFilterModel
from bakedpytato.task.base_task import BaseTask


logger = logging.getLogger(__name__)

class BaseSupplierCatalogTask(BaseTask):
	
	def load_plugins(self):
		"""Load Plugins"""
		plugins = dict()
		query = self.session.query(SupplierCatalogFilterModel)
		for supplier_catalog_filter in query:
			plugin_name = supplier_catalog_filter.name + 'Plugin'
			if plugin_name in vars(plugin):
				SupplierCatalogPlugin = getattr(plugin, plugin_name)
				plug = SupplierCatalogPlugin(supplier_catalog_filter)
				plugins[supplier_catalog_filter.id] = plug
				plugins[supplier_catalog_filter.supplier_id] = plug
			else:
				logger.warning("Plugin %s Not Found", plugin_name)
		return plugins
