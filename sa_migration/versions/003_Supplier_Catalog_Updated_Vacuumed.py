from sqlalchemy import *
from migrate import *

import logging

logger = logging.getLogger(__name__)

def upgrade(migrate_engine):
	# Upgrade operations go here. Don't create your own engine; bind
	# migrate_engine to your metadata
	pass
	meta = MetaData(bind=migrate_engine, reflect=True)

	supplier_catalog = Table('supplier_catalogs', meta, autoload=True)
	if 'supplier_catalog_item_versions_loaded' not in supplier_catalog.c:
		supplier_catalog_item_versions_loaded = Column('supplier_catalog_item_versions_loaded', DateTime)
		supplier_catalog_item_versions_loaded.create(supplier_catalog)
	if 'updated' not in supplier_catalog.c:
		updated = Column('updated', DateTime)
		updated.create(supplier_catalog)
	if 'vacuumed' not in supplier_catalog.c:
		vacuumed = Column('vacuumed', DateTime)
		vacuumed.create(supplier_catalog)

	supplier_catalog_item_field = Table('supplier_catalog_item_fields', meta, autoload=True)
	if 'updated' not in supplier_catalog_item_field.c:
		updated = Column('updated', DateTime)
		updated.create(supplier_catalog_item_field)
	if 'vacuumed' not in supplier_catalog_item_field.c:
		vacuumed = Column('vacuumed', DateTime)
		vacuumed.create(supplier_catalog_item_field)

	supplier_catalog_item = Table('supplier_catalog_items', meta, autoload=True)
	if 'updated' not in supplier_catalog_item.c:
		updated = Column('updated', DateTime)
		updated.create(supplier_catalog_item)
	if 'vacuumed' not in supplier_catalog_item.c:
		vacuumed = Column('vacuumed', DateTime)
		vacuumed.create(supplier_catalog_item)

	for plugin in ['bowser', 'emery', 'exactrail', 'heartland', 'walthers']:
		supplier_catalog_item_version = Table('supplier_catalog_item_' + plugin + '_versions', meta, autoload=True)
		if 'updated' not in supplier_catalog_item_version.c:
			updated = Column('updated', DateTime)
			updated.create(supplier_catalog_item_version)
		if 'vacuumed' not in supplier_catalog_item_version.c:
			vacuumed = Column('vacuumed', DateTime)
			vacuumed.create(supplier_catalog_item_version)




def downgrade(migrate_engine):
	# Operations to reverse the above upgrade go here.
	pass
	
	meta = MetaData(bind=migrate_engine, reflect=True)
	
	supplier_catalog = Table('supplier_catalogs', meta, autoload=True)
	if 'supplier_catalog_item_versions_loaded' in supplier_catalog.c:
		supplier_catalog.c.supplier_catalog_item_versions_loaded.drop()
	if 'updated' in supplier_catalog.c:
		supplier_catalog.c.updated.drop()
	if 'vacuumed' in supplier_catalog.c:
		supplier_catalog.c.vacuumed.drop()

	supplier_catalog_item_field = Table('supplier_catalog_item_fields', meta, autoload=True)
	if 'updated' in supplier_catalog_item_field.c:
		supplier_catalog_item_field.c.updated.drop()
	if 'vacuumed' in supplier_catalog_item_field.c:
		supplier_catalog_item_field.c.vacuumed.drop()
	
	supplier_catalog_item = Table('supplier_catalog_item_fields', meta, autoload=True)
	if 'updated' in supplier_catalog_item.c:
		supplier_catalog_item.c.updated.drop()
	if 'vacuumed' in supplier_catalog_item.c:
		supplier_catalog_item.c.vacuumed.drop()

	for plugin in ['bowser', 'emery', 'exactrail', 'heartland', 'walthers']:
		supplier_catalog_item_version = Table('supplier_catalog_item_' + plugin + '_versions', meta, autoload=True)
		if 'updated' in supplier_catalog_item_version.c:
			supplier_catalog_item_version.c.updated.drop()
		if 'vacuumed' in supplier_catalog_item_version.c:
			supplier_catalog_item_version.c.vacuumed.drop()
