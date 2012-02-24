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
#Pragma
from __future__ import unicode_literals
#Standard Library
import pkgutil
#Extended Library
#Application Library
from bakedpytato import cfg, model, plugin, task
"""
Allow individual model, plugin, task, classes 
to be coded each in individual module files 
and loaded dynamically

example:
	file 'bakedpytato/model/generic_model'
should contain
	def GenericModel(BaseModel):

becomes accessible as
	x = bakedpytato.model.GenericModel()
	
classes are also added to the sub-package's __ALL__:
	from bakedpytato.model import *
	x = GenericModel()

Base classes are excluded:
	file 'bakedpytato/model/base_model'
	x = bakedpytato.model.base_model.BaseModel()
	but not 
	x = bakedpytato.model.BaseModel()
"""

for module, path, module_suffix, class_suffix in [
	[model, 'bakedpytato/model', 'model', 'Model'], 
	[plugin, 'bakedpytato/plugin', 'plugin', 'Plugin'], 
	[task, 'bakedpytato/task', 'task', 'Task']
]:
	ALL = getattr(module, '__ALL__')
	for module_loader, package_name, ispkg in pkgutil.iter_modules([path]):
		if package_name.startswith('base'):
			continue
		if not package_name.endswith(module_suffix):
			continue
		full_package_name = "%s.%s" % (__name__, package_name)
		sub_module = module_loader.find_module(package_name).load_module(full_package_name)
		for attr in dir(sub_module):
			obj = getattr(sub_module, attr)
			if attr.startswith('Base'):
				continue
			if not attr.endswith(class_suffix):
				continue
			setattr(module, attr, obj)
			ALL.append(obj)

