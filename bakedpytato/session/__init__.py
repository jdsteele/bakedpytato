#Pragma
from __future__ import unicode_literals

from bakedpytato import cfg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(cfg.sql_url, echo=False)
Session = sessionmaker(bind=engine, autocommit=False)

def local_engine():
	return create_engine(cfg.sql_local_url, echo=False, strategy='threadlocal')

def remote_engine():
	return create_engine(cfg.sql_remote_url, echo=False, strategy='threadlocal')
