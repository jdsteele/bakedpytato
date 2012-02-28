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
from bakedpytato.model import SupplierSpecialFilterModel
from bakedpytato.task.base_task import BaseTask


logger = logging.getLogger(__name__)

class BaseSupplierSpecialTask(BaseTask):
	
	def load_plugins(self):
		"""Load Plugins"""
		plugins = dict()
		query = self.session.query(SupplierSpecialFilterModel)
		for supplier_special_filter in query:
			plugin_name = supplier_special_filter.name + 'Plugin'
			if plugin_name in vars(plugin):
				PluginClass = getattr(plugin, plugin_name)
				plugins[supplier_special_filter.id] = PluginClass(supplier_special_filter)
			else:
				logger.warning("Plugin %s Not Found", plugin_name)
		return plugins
