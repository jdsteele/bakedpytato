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

import pkgutil

__all__ = []

for importer, package_name, _ in pkgutil.iter_modules([__name__]):
	if package_name.startswith('base_'):
		continue
	if not package_name.endswith(__name__):
		continue
	full_package_name = __name__ + ('.%s' % package_name)
	module = importer.find_module(package_name).load_module(full_package_name)
	for attr in dir(module):
		if attr.startswith('Base'):
			continue
		if not attr.endswith(__name__.capitalize()):
			continue
		clsobj = getattr(module, attr)
		__all__.append(attr)
		globals()[attr] = clsobj
