from sqlalchemy import *
from migrate import *

import logging

logger = logging.getLogger(__name__)

def upgrade(migrate_engine):
	# Upgrade operations go here. Don't create your own engine; bind
	# migrate_engine to your metadata
	meta = MetaData(bind=migrate_engine, reflect=True)

	supplier_catalog = Table('supplier_catalogs', meta, autoload=True)
	if 'encoding' not in supplier_catalog.c:
		encoding = Column('encoding', String)
		encoding.create(supplier_catalog)

def downgrade(migrate_engine):
	# Operations to reverse the above upgrade go here.
	
	meta = MetaData(bind=migrate_engine, reflect=True)
	
	supplier_catalog = Table('supplier_catalogs', meta, autoload=True)
	if 'encoding' in supplier_catalog.c:
		supplier_catalog.c.encoding.drop()
