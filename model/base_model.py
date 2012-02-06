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

from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base, declared_attr

#from environment import Base

BaseModel = declarative_base()

import time
import uuid

class UUIDMixin(object):
	@declared_attr
	def id(cls):
		return Column(
			UUID(as_uuid=True), 
			primary_key=True, 
			default=uuid.uuid4, 
			unique=True
		)

class TimestampMixin(object):
	
	@declared_attr
	def created(cls):
		return Column(
			DateTime, 
			default=time.strftime('%Y-%m-%d %H:%M:%S %Z')
		)

	@declared_attr
	def modified(cls):
		return Column(
			DateTime, 
			default=time.strftime('%Y-%m-%d %H:%M:%S %Z'),
			onupdate=time.strftime('%Y-%m-%d %H:%M:%S %Z')
		)

class DefaultMixin(UUIDMixin, TimestampMixin):
	pass

