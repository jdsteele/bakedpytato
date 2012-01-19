from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base, declared_attr

#from environment import Base

Base = declarative_base()

import time
import uuid

class UUIDMixin(object):
	@declared_attr
	def id(cls):
		return Column(UUID(), primary_key=True, default=uuid.uuid4, unique=True)


class TimestampMixin(object):
	_debug = False
	
	@declared_attr
	def created(cls):
		return Column(DateTime, default=time.strftime('%Y-%m-%d %H:%M:%S %Z'))

	@declared_attr
	def modified(cls):
		return Column(DateTime, default=time.strftime('%Y-%m-%d %H:%M:%S %Z'))

	def __setattr__(self, name, value):
		#print self, name, value
		if (
			not name.startswith('_') and 
			name != 'modified'
		):
			old_value = object.__getattribute__(self, name)
			if value != old_value:
				if self._debug:
					print('DIRTY', self, name, old_value, value)
				object.__setattr__(self, '_dirty', True)
				object.__setattr__(self, 'modified', time.strftime('%Y-%m-%d %H:%M:%S %Z'))
				return object.__setattr__(self, name, value)
			return
		return object.__setattr__(self, name, value)

	def is_dirty(self):
		return self._dirty

	def set_debug(self, debug):
		self._debug = debug


class DefaultMixin(UUIDMixin, TimestampMixin):
	pass

