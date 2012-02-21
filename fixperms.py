#!/usr/bin/env python
#Pragma
from __future__ import unicode_literals

import os
import pwd
import grp
import stat

tops = ['/var/www/bakedpytato', '/var/log/bakedpytato']

executables = [
	'test.py', 
	'update_all.py', 
	'fixperms.py', 
	'mirror.py',
	'force_load_walthers_catalog.py',
	'manage.py'
]

file_owner = pwd.getpwnam('www-data')[2]
file_group = grp.getgrnam('www-data')[2]
file_perm = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP

dir_owner = pwd.getpwnam('www-data')[2]
dir_group = grp.getgrnam('www-data')[2]
dir_perm = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP

exe_owner = pwd.getpwnam('www-data')[2]
exe_group = grp.getgrnam('www-data')[2]
exe_perm = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IXGRP

for top in tops:
	os.chown(top, dir_owner, dir_group)
	os.chmod(top, dir_perm)
	for (dirpath, dirnames, filenames) in os.walk(top, topdown=True, onerror=None, followlinks=False):
		for dirname in dirnames:
			path = os.path.join(dirpath, dirname)
			os.chown(path, dir_owner, dir_group)
			os.chmod(path, dir_perm)

		for filename in filenames:
			path = os.path.join(dirpath, filename)
			if filename in executables:
				os.chown(path, exe_owner, exe_group)
				os.chmod(path, exe_perm)
			else:
				os.chown(path, file_owner, file_group)
				os.chmod(path, file_perm)
