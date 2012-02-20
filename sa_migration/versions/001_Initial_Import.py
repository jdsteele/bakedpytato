from sqlalchemy import *
from sqlalchemy import exc
from migrate import *
from migrate.changeset.schema import *
from sqlalchemy.dialects.postgresql import UUID
from decimal import *

import logging

logger = logging.getLogger(__name__)

data = list()

data.append({
	'name':'address_countries',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'name', 'type_':String, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'address_provinces',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'name', 'type_':String, 'nullable':True},
		{'name':'address_country_id', 'type_':UUID(), 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'addresses',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'street_1', 'type_':String, 'nullable':True},
		{'name':'street_2', 'type_':String, 'nullable':True},
		{'name':'address_country_id', 'type_':UUID, 'nullable':True},
		{'name':'address_province_id', 'type_':UUID, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'barcode_conversions',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'regex', 'type_':String, 'nullable':True},
		{'name':'match_class', 'type_':String, 'nullable':True},
		{'name':'match_1', 'type_':String, 'nullable':True},
		{'name':'match_2', 'type_':String, 'nullable':True},
		{'name':'match_3', 'type_':String, 'nullable':True},
		{'name':'notes', 'type_':String, 'nullable':True},
		{'name':'multiplier', 'type_':Numeric, 'nullable':False, 'server_default':'0'},
		{'name':'condition_1_name', 'type_':String, 'nullable':True},
		{'name':'condition_1_value', 'type_':String, 'nullable':True},
		{'name':'condition_2_name', 'type_':String, 'nullable':True},
		{'name':'condition_2_value', 'type_':String, 'nullable':True},
		{'name':'condition_3_name', 'type_':String, 'nullable':True},
		{'name':'condition_3_value', 'type_':String, 'nullable':True},
		{'name':'output_class', 'type_':String, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'cake_sessions',
	'columns': [
		{'name':'id', 'type_':String, 'length':255, 'primary_key':True,'nullable':False},
		{'name':'data', 'type_':String, 'nullable':True},
		{'name':'expires', 'type_':Integer, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True}
	],
})

data.append({
	'name':'catalog_categories',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'scale_id', 'type_':UUID, 'nullable':True},
		{'name':'manufacturer_id', 'type_':UUID, 'nullable':True},
		{'name':'category_id', 'type_':Integer, 'nullable':True},
		{'name':'catalog_item_count', 'type_':Integer, 'nullable':True},
		{'name':'category_sort', 'type_':Integer, 'nullable':True},
		{'name':'manufacturer_sort', 'type_':Integer, 'nullable':True},
		{'name':'aacart_cat', 'type_':String, 'nullable':True},
		{'name':'special', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'advanced', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True}
	],
})

data.append({
	'name':'catalog_items',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'aacart_cat1', 'type_':String, 'nullable':True},
		{'name':'aacart_cat2', 'type_':String, 'nullable':True},
		{'name':'aacart_cat3', 'type_':String, 'nullable':True},
		{'name':'aacart_description', 'type_':String, 'nullable':True},
		{'name':'aacart_discount', 'type_':Integer, 'nullable':True},
		{'name':'aacart_listprice', 'type_':String, 'nullable':True},
		{'name':'aacart_man', 'type_':String, 'nullable':False},
		{'name':'aacart_name', 'type_':String, 'nullable':True},
		{'name':'aacart_part', 'type_':String, 'nullable':False},
		{'name':'aacart_saleprice', 'type_':Numeric, 'nullable':False, 'server_default':'0'},
		{'name':'aacart_stock', 'type_':Numeric, 'nullable':False, 'server_default':'0'},
		{'name':'advanced', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'category_id', 'type_':Integer, 'nullable':True},
		{'name':'category_id_2', 'type_':Integer, 'nullable':True},
		{'name':'cost', 'type_':Numeric, 'nullable':False, 'server_default':'0'},
		{'name':'deleted', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'display', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'force_in_stock', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'manufacturer_id', 'type_':UUID, 'nullable':True},
		{'name':'notes', 'type_':String, 'nullable':True},
		{'name':'phased_out', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'product_id', 'type_':UUID, 'nullable':False},
		{'name':'product_package', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'ranking_supplier_id', 'type_':UUID, 'nullable':True},
		{'name':'reason', 'type_':String, 'nullable':True},
		{'name':'scale_id', 'type_':UUID, 'nullable':True},
		{'name':'sort', 'type_':Integer, 'nullable':False, 'server_default':'0'},
		{'name':'stock', 'type_':Numeric, 'nullable':False, 'server_default':'0'},
		{'name':'supplier_advanced', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'supplier_available', 'type_':Date, 'nullable':True},
		{'name':'supplier_cost', 'type_':Numeric, 'nullable':True, 'server_default':'0'},
		{'name':'supplier_id', 'type_':UUID, 'nullable':True},
		{'name':'supplier_retail', 'type_':Numeric, 'nullable':True, 'server_default':'0'},
		{'name':'supplier_sale', 'type_':Numeric, 'nullable':True, 'server_default':'0'},
		{'name':'supplier_special', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'supplier_stock', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True}
	],
})

data.append({
	'name':'categories',
	'columns': [
		{'name':'id', 'type_':Integer, 'primary_key':True,'nullable':False},
		{'name':'catalog_category_count', 'type_':Integer, 'nullable':True},
		{'name':'category_conversion_count', 'type_':Integer, 'nullable':True},
		{'name':'catalog_item_count', 'type_':Integer, 'nullable':True},
		{'name':'level', 'type_':Integer, 'nullable':True},
		{'name':'lft', 'type_':Integer, 'nullable':True},
		{'name':'name', 'type_':String, 'nullable':False},
		{'name':'parent_id', 'type_':Integer, 'nullable':True},
		{'name':'pathx', 'type_':String, 'nullable':True},
		{'name':'product_count', 'type_':Integer, 'nullable':True},
		{'name':'rght', 'type_':Integer, 'nullable':True},
		{'name':'root_id', 'type_':Integer, 'nullable':True},
		{'name':'walthers_cat', 'type_':Integer, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'category_conversions',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'category_id', 'type_':Integer, 'nullable':True},
		{'name':'manufacturer_id', 'type_':UUID, 'nullable':True},
		{'name':'needle', 'type_':String, 'nullable':True},
		{'name':'rank', 'type_':Integer, 'nullable':False, 'server_default':'1'},
		{'name':'supplier_id', 'type_':UUID, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'cron_jobs',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'completed', 'type_':DateTime, 'nullable':True},
		{'name':'cron_tab_id', 'type_':UUID, 'nullable':False},
		{'name':'effective', 'type_':DateTime, 'nullable':True},
		{'name':'pid', 'type_':Integer, 'nullable':True},
		{'name':'return_value', 'type_':Integer, 'nullable':True},
		{'name':'started', 'type_':DateTime, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
	],
})

data.append({
	'name':'cron_tabs',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'enabled', 'type_':Boolean, 'nullable':False, 'server_default':'True'},
		{'name':'interval', 'type_':String, 'nullable':False},
		{'name':'name', 'type_':String, 'nullable':True},
		{'name':'order', 'type_':Integer, 'nullable':True},
		{'name':'task_method', 'type_':String, 'nullable':False},
		{'name':'task_name', 'type_':String, 'nullable':False},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'customer_incidentals',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'name', 'type_':String, 'nullable':True},
		{'name':'serial', 'type_':Integer, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'customer_order_fields',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'fields', 'type_':Binary, 'nullable':True},
		{'name':'file_import_id', 'type_':UUID, 'nullable':False},
		{'name':'filter', 'type_':String, 'nullable':True},
		{'name':'row_number', 'type_':Integer, 'nullable':False},
		{'name':'source', 'type_':String, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
	],
})

data.append({
	'name':'customer_order_incidentals',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'customer_incidental_id', 'type_':UUID, 'nullable':True},
		{'name':'customer_order_id', 'type_':UUID, 'nullable':True},
		{'name':'mutable', 'type_':Boolean, 'nullable':False, 'server_default':'True'},
		{'name':'price', 'type_':Numeric, 'nullable':True},
		{'name':'serial', 'type_':Integer, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'customer_order_item_versions',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
	],
})

data.append({
	'name':'customer_order_items',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'customer_order_id', 'type_':UUID, 'nullable':False},
		{'name':'customer_shipment_item_count', 'type_':Integer, 'nullable':True},
		{'name':'external', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'legacy_flag', 'type_':Integer, 'nullable':False, 'server_default':'0'},
		{'name':'line_number', 'type_':Integer, 'nullable':True},
		{'name':'lock', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'mutable', 'type_':Boolean, 'nullable':False, 'server_default':'True'},
		{'name':'price', 'type_':Numeric, 'nullable':True},
		{'name':'product_id', 'type_':UUID, 'nullable':True},
		{'name':'quantity', 'type_':Numeric, 'nullable':True},
		{'name':'serial', 'type_':Integer, 'nullable':True},
		{'name':'text', 'type_':String, 'nullable':True},
		{'name':'void', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'customer_order_sources',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'customer_order_count', 'type_':Integer, 'nullable':True},
		{'name':'name', 'type_':String, 'nullable':False},
		{'name':'serial', 'type_':Integer, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'customer_order_versions',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'customer_address_1', 'type_':String, 'nullable':True},
		{'name':'customer_address_2', 'type_':String, 'nullable':True},
		{'name':'customer_city', 'type_':String, 'nullable':True},
		{'name':'customer_country', 'type_':String, 'nullable':True},
		{'name':'customer_email', 'type_':String, 'nullable':True},
		{'name':'customer_name', 'type_':String, 'nullable':True},
		{'name':'customer_order_field_id', 'type_':UUID, 'nullable':True},
		{'name':'customer_phone', 'type_':String, 'nullable':True},
		{'name':'customer_state', 'type_':String, 'nullable':True},
		{'name':'customer_zip', 'type_':String, 'nullable':True},
		{'name':'identifier', 'type_':String, 'nullable':True},
		{'name':'ordered date', 'type_':Date, 'nullable':True},
		{'name':'payment_identifier', 'type_':String, 'nullable':True},
		{'name':'row_number', 'type_':Integer, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
	],
})

data.append({
	'name':'customer_orders',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'billing_address', 'type_':String, 'nullable':True},
		{'name':'billing_address_1', 'type_':String, 'nullable':True},
		{'name':'billing_address_2', 'type_':String, 'nullable':True},
		{'name':'billing_city', 'type_':String, 'nullable':True},
		{'name':'billing_company', 'type_':String, 'nullable':True},
		{'name':'billing_country', 'type_':String, 'nullable':True},
		{'name':'billing_state', 'type_':String, 'nullable':True},
		{'name':'billing_zip', 'type_':String, 'nullable':True},
		{'name':'closed', 'type_':Date, 'nullable':True},
		{'name':'customer_email', 'type_':String, 'nullable':True},
		{'name':'customer_name', 'type_':String, 'nullable':True},
		{'name':'customer_id', 'type_':UUID, 'nullable':True},
		{'name':'customer_order_item_count', 'type_':Integer, 'nullable':True},
		{'name':'customer_order_item_quantity', 'type_':Integer, 'nullable':True},
		{'name':'customer_order_source_id', 'type_':UUID, 'nullable':True},
		{'name':'customer_orders_customer_payment_count', 'type_':Integer, 'nullable':True},
		{'name':'customer_orders_customer_shipment_count', 'type_':Integer, 'nullable':True},
		{'name':'customer_phone', 'type_':String, 'nullable':True},
		{'name':'customer_shipment_item_quantity', 'type_':Integer, 'nullable':True},
		{'name':'external', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'flagged', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'identifier', 'type_':String, 'nullable':True},
		{'name':'legacy_flag', 'type_':Integer, 'nullable':False, 'server_default':'0'},
		{'name':'mutable', 'type_':Boolean, 'nullable':False, 'server_default':'True'},
		{'name':'open_flag', 'type_':Integer, 'nullable':False, 'server_default':'1'},
		{'name':'ordered', 'type_':Date, 'nullable':True},
		{'name':'serial', 'type_':Integer, 'nullable':True},
		{'name':'shipping_address', 'type_':String, 'nullable':True},
		{'name':'shipping_address_1', 'type_':String, 'nullable':True},
		{'name':'shipping_address_2', 'type_':String, 'nullable':True},
		{'name':'shipping_city', 'type_':String, 'nullable':True},
		{'name':'shipping_company', 'type_':String, 'nullable':True},
		{'name':'shipping_country', 'type_':String, 'nullable':True},
		{'name':'shipping_state', 'type_':String, 'nullable':True},
		{'name':'shipping_zip', 'type_':String, 'nullable':True},
		{'name':'void', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'warehouse_id', 'type_':UUID, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})


data.append({
	'name':'customer_orders_customer_payments',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'customer_order_id', 'type_':UUID, 'nullable':True},
		{'name':'customer_payment_id', 'type_':UUID, 'nullable':True},
		{'name':'lock', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'mutable', 'type_':Boolean, 'nullable':False, 'server_default':'True'},
		{'name':'price', 'type_':Numeric, 'nullable':True},
		{'name':'serial', 'type_':Integer, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})


data.append({
	'name':'customer_orders_customer_shipments',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'customer_order_id', 'type_':UUID, 'nullable':True},
		{'name':'customer_shipment_id', 'type_':UUID, 'nullable':True},
		{'name':'legacy_flag', 'type_':Integer, 'nullable':True, 'server_default':'0'},
		{'name':'lock', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'mutable', 'type_':Boolean, 'nullable':False, 'server_default':'True'},
		{'name':'serial', 'type_':Integer, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'customer_payment_sources',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'name', 'type_':String, 'nullable':True},
		{'name':'serial', 'type_':Integer, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'customer_payments',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'customer_identifier', 'type_':String, 'nullable':True},
		{'name':'customer_order_identifier', 'type_':String, 'nullable':True},
		{'name':'customer_payment_source_id', 'type_':UUID, 'nullable':True},
		{'name':'date_time', 'type_': DateTime, 'nullable':True},
		{'name':'fee', 'type_': Numeric, 'nullable':True},
		{'name':'gross', 'type_': Numeric, 'nullable':True},
		{'name':'identifier', 'type_': String, 'nullable':True},
		{'name':'legacy_flag', 'type_': Integer, 'nullable':True},
		{'name':'mutable', 'type_': Boolean, 'nullable':False, 'server_default':'True'},
		{'name':'net', 'type_': Numeric, 'nullable':True},
		{'name':'serial', 'type_': Integer, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'customer_shipment_items',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'customer_order_id', 'type_':UUID,'nullable':False},
		{'name':'customer_order_item_id', 'type_':UUID, 'nullable':True},
		{'name':'customer_shipment_id', 'type_':UUID,'nullable':False},
		{'name':'legacy_flag', 'type_':Integer, 'nullable':False, 'server_default':'0'},
		{'name':'mutable', 'type_':Boolean, 'nullable':False, 'server_default':'True'},
		{'name':'product_id', 'type_':UUID, 'nullable':True},
		{'name':'quantity', 'type_':Numeric, 'nullable':False},
		{'name':'serial', 'type_':Integer, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'customer_shipments',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'warehouse_id', 'type_':UUID, 'nullable':False},
		{'name':'shipped', 'type_':Date, 'nullable':True},
		{'name':'label', 'type_':String, 'nullable':True},
		{'name':'identifier', 'type_':String, 'nullable':True},
		{'name':'shipper_id', 'type_':UUID, 'nullable':True},
		{'name':'postage', 'type_':Numeric, 'nullable':True},
		{'name':'insurance', 'type_':Numeric, 'nullable':True},
		{'name':'weight', 'type_':String, 'nullable':True},
		{'name':'name', 'type_':String, 'nullable':True},
		{'name':'address', 'type_':String, 'nullable':True},
		{'name':'legacy_flag', 'type_':Integer, 'nullable':False, 'server_default':'0'},
		{'name':'customer_order_identifier', 'type_':String, 'nullable':True},
		{'name':'void', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'mutable', 'type_':Boolean, 'nullable':False, 'server_default':'True'},
		{'name':'customer_shipment_item_count', 'type_':Integer, 'nullable':True},
		{'name':'serial', 'type_':Integer, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'customers',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'name', 'type_':String, 'nullable':True},
		{'name':'blob', 'type_':String, 'nullable':True},
		{'name':'metaphone', 'type_':String, 'nullable':True},
		{'name':'soundex', 'type_':String, 'nullable':True},
		{'name':'email', 'type_':String, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})


data.append({
	'name':'file_imports',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'content', 'type_':Binary, 'nullable':False},
		{'name':'effective', 'type_':DateTime, 'nullable':True},
		{'name':'lock_issue_date', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'mutable', 'type_':Boolean, 'nullable':False, 'server_default':'True'},
		{'name':'name', 'type_':String, 'nullable':True},
		{'name':'sha256', 'type_':String, 'length':64, 'nullable':True},
		{'name':'size', 'type_':Integer, 'nullable':False, 'server_default':'0'},
		{'name':'supplier_catalog_count', 'type_':Integer, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'groups',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'name', 'type_':String, 'nullable':True},
		{'name':'serial', 'type_':Integer, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'images',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'content', 'type_':Binary, 'nullable':False},
		{'name':'height', 'type_':Integer, 'nullable':True},
		{'name':'name', 'type_':String, 'nullable':True},
		{'name':'sha256', 'type_':String, 'length':64, 'nullable':False},
		{'name':'size', 'type_':Integer, 'nullable':True},
		{'name':'type', 'type_':String, 'nullable':True},
		{'name':'width', 'type_':Integer, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'inventory_audit_items',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'inventory_audit_id', 'type_':UUID, 'nullable':True},
		{'name':'product_id', 'type_':UUID, 'nullable':True},
		{'name':'shrink', 'type_':Numeric, 'nullable':True},
		{'name':'quantity', 'type_':Numeric, 'nullable':True},
		{'name':'absolute', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'serial', 'type_':Integer, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'inventory_audits',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'warehouse_id', 'type_':UUID,'nullable':True},
		{'name':'audited', 'type_':Date,'nullable':True},
		{'name':'name', 'type_':String,'nullable':True},
		{'name':'inventory_audit_item_count', 'type_':Integer,'nullable':True},
		{'name':'serial', 'type_':Integer,'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'inventory_items',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'product_id', 'type_':UUID,'nullable':False},
		{'name':'quantity', 'type_':Numeric,'nullable':False},
		{'name':'warehouse_id', 'type_':UUID,'nullable':False},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
	],
})

data.append({
	'name':'inventory_level_controls',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'lead', 'type_':Numeric, 'nullable':True},
		{'name':'order', 'type_':Numeric, 'nullable':True},
		{'name':'product_id', 'type_':UUID, 'nullable':True},
		{'name':'safety', 'type_':Numeric, 'nullable':False, 'server_default':'0'},
		{'name':'warehouse_id', 'type_':UUID, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'inventory_transactions',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'balance', 'type_':Numeric, 'nullable':True},
		{'name':'customer_order_id', 'type_':UUID, 'nullable':True},
		{'name':'customer_order_item_id', 'type_':UUID, 'nullable':True},
		{'name':'customer_shipment_id', 'type_':UUID, 'nullable':True},
		{'name':'customer_shipment_item_id', 'type_':UUID, 'nullable':True},
		{'name':'date', 'type_':Date, 'nullable':False},
		{'name':'inventory_audit_id', 'type_':UUID, 'nullable':True},
		{'name':'inventory_audit_item_id', 'type_':UUID, 'nullable':True},
		{'name':'inventory_transfer_id', 'type_':UUID, 'nullable':True},
		{'name':'inventory_transfer_item_id', 'type_':UUID, 'nullable':True},
		{'name':'product_id', 'type_':UUID, 'nullable':True},
		{'name':'product_package_id', 'type_':UUID, 'nullable':True},
		{'name':'quantity', 'type_':Numeric, 'nullable':True},
		{'name':'supplier_order_id', 'type_':UUID, 'nullable':True},
		{'name':'supplier_order_item_id', 'type_':UUID, 'nullable':True},
		{'name':'supplier_shipment_id', 'type_':UUID, 'nullable':True},
		{'name':'supplier_shipment_item_id', 'type_':UUID, 'nullable':True},
		{'name':'type', 'type_':String, 'nullable':True},
		{'name':'unshipped_balance', 'type_':Numeric, 'nullable':True},
		{'name':'warehouse_id', 'type_':UUID, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
	],
})

data.append({
	'name':'inventory_transfer_items',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'inventory_transfer_id', 'type_':UUID, 'nullable':False},
		{'name':'product_id', 'type_':UUID, 'nullable':False},
		{'name':'quantity', 'type_':Numeric, 'nullable':False, 'server_default':'0'},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'inventory_transfers',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'date', 'type_':Date,'nullable':False},
		{'name':'from_warehouse_id', 'type_':UUID, 'nullable':False},
		{'name':'inventory_transfer_item_count', 'type_':Integer, 'nullable':True},
		{'name':'to_warehouse_id', 'type_':UUID, 'nullable':False},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'manufacturer_conversions',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'customer_order_source_id', 'type_':UUID, 'nullable':True},
		{'name':'lock', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'manufacturer_id', 'type_':UUID, 'nullable':True},
		{'name':'manufacturer_identifier', 'type_':String, 'nullable':True},
		{'name':'supplier_id', 'type_':UUID, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'manufacturers',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'catalog_category_count', 'type_':Integer, 'nullable':True},
		{'name':'catalog_item_count', 'type_':Integer, 'nullable':True},
		{'name':'category_conversion_count', 'type_':Integer, 'nullable':True},
		{'name':'default_product_url', 'type_':String, 'nullable':True},
		{'name':'default_product_image_url', 'type_':String, 'nullable':True},
		{'name':'display', 'type_':Boolean, 'nullable':False, 'server_default':'True'},
		{'name':'enabled', 'type_':Boolean, 'nullable':False, 'server_default':'False'},
		{'name':'identifier', 'type_':String, 'nullable':True},
		{'name':'manufacturer_conversion_count', 'type_':Integer, 'nullable':True},
		{'name':'name', 'type_':String, 'nullable':True},
		{'name':'product_count', 'type_':Integer, 'nullable':True},
		{'name':'short_name', 'type_':String, 'nullable':True},
		{'name':'supplier_catalog_item_count', 'type_':Integer, 'nullable':True},
		{'name':'sort', 'type_':Integer, 'nullable':True},
		{'name':'url', 'type_':String, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'payment_sources',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'name', 'type_':String, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'payments',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'payment_source_id', 'type_':UUID, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'price_controls',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'allow_preorder', 'type_':Boolean, 'nullable':False},
		{'name':'cost_ratio', 'type_':Numeric, 'nullable':False, 'server_default':'110'},
		{'name':'enable', 'type_':Boolean, 'nullable':False, 'server_default':'True'},
		{'name':'manufacturer_id', 'type_':UUID, 'nullable':True},
		{'name':'normal', 'type_':Boolean, 'nullable':False, 'server_default':'True'},
		{'name':'preorder', 'type_':Boolean, 'nullable':False, 'server_default':'True'},
		{'name':'rank', 'type_':Integer, 'nullable':True},
		{'name':'retail_high', 'type_':Numeric, 'nullable':False, 'server_default':'NaN'},
		{'name':'retail_low', 'type_':Numeric, 'nullable':False, 'server_default':'0'},
		{'name':'retail_ratio', 'type_':Numeric, 'nullable':False, 'server_default':'100'},
		{'name':'rubber_ratio', 'type_':Numeric, 'nullable':False, 'server_default':'60'},
		{'name':'special', 'type_':Boolean, 'nullable':False, 'server_default':'True'},
		{'name':'supplier_id', 'type_':UUID, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'processes',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'task', 'type_':String, 'nullable':True},
		{'name':'function', 'type_':String, 'nullable':True},
		{'name':'parameter', 'type_':String, 'nullable':True},
		{'name':'priority', 'type_':Integer, 'nullable':False, 'server_default':'1'},
		{'name':'pid', 'type_':Integer, 'nullable':True},
		{'name':'memory', 'type_':Integer, 'nullable':True},
		{'name':'requested', 'type_':Numeric, 'nullable':True},
		{'name':'started', 'type_':Numeric, 'nullable':True},
		{'name':'completed', 'type_':Numeric, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
	],
})

data.append({
	'name':'product_barcodes',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'product_id', 'type_':UUID, 'nullable':False},
		{'name':'barcode', 'type_':String, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'product_conversion_regexes',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'supplier_id', 'type_':UUID, 'nullable':True},
		{'name':'manufacturer_id', 'type_':UUID, 'nullable':True},
		{'name':'needle', 'type_':String, 'nullable':True},
		{'name':'haystack', 'type_':String, 'nullable':True},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})

data.append({
	'name':'product_conversions',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True,'nullable':False},
		{'name':'customer_order_source_id', 'type_':UUID, 'nullable':True},
		{'name':'lock', 'type_':Boolean, 'nullable':False, 'server_default':'false'},
		{'name':'product_id', 'type_':UUID, 'nullable':True},
		{'name':'product_identifier', 'type_':String, 'nullable':True},
		{'name':'manufacturer_id', 'type_':UUID, 'nullable':True},
		{'name':'source_quantity', 'type_':Numeric, 'nullable':False, 'server_default':'1'},
		{'name':'supplier_id', 'type_':UUID, 'nullable':True},
		{'name':'target_quantity', 'type_':Numeric, 'nullable':False, 'server_default':'1'},
		{'name':'created', 'type_':DateTime, 'nullable':True},
		{'name':'modified', 'type_':DateTime, 'nullable':True},
		{'name':'creator_id', 'type_':UUID, 'nullable':True},
		{'name':'modifier_id', 'type_':UUID, 'nullable':True},
	],
})


data.append({
	'name':'product_daily_stats',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True, 'nullable':False},
		{'name':'customer_order_quantity', 'type_':Numeric, 'nullable':True},
		{'name':'customer_order_total', 'type_':Numeric, 'nullable':True},
		{'name':'customer_shipment_quantity', 'type_':Numeric, 'nullable':True},
		{'name':'customer_shipment_total', 'type_':Numeric, 'nullable':True},
		{'name':'date', 'type_':Date, 'nullable':False},
		{'name':'inventory_audit_shrink', 'type_':Numeric, 'nullable':True},
		{'name':'inventory_audit_total', 'type_':Numeric, 'nullable':True},
		{'name':'product_id', 'type_':UUID, 'nullable':False},
		{'name':'supplier_shipment_quantity', 'type_':Numeric, 'nullable':True},
		{'name':'supplier_shipment_total', 'type_':Numeric, 'nullable':True},
	],
})

data.append({
	'name':'product_monthly_stats',
	'columns': [
		{'name':'id', 'type_':UUID, 'primary_key':True, 'nullable':False},
		{'name':'customer_order_quantity', 'type_':Numeric, 'nullable':True},
		{'name':'customer_order_total', 'type_':Numeric, 'nullable':True},
		{'name':'customer_shipment_quantity', 'type_':Numeric, 'nullable':True},
		{'name':'customer_shipment_total', 'type_':Numeric, 'nullable':True},
		{'name':'inventory_audit_shrink', 'type_':Numeric, 'nullable':True},
		{'name':'inventory_audit_total', 'type_':Numeric, 'nullable':True},
		{'name':'month', 'type_':Integer, 'nullable':False},
		{'name':'product_id', 'type_':UUID, 'nullable':False},
		{'name':'supplier_shipment_quantity', 'type_':Numeric, 'nullable':True},
		{'name':'supplier_shipment_total', 'type_':Numeric, 'nullable':True},
		{'name':'year', 'type_':Integer, 'nullable':False},
	],
})

data.append({
	'name':'product_packages',
	'columns': [
		{'name': 'id', 'type_':UUID, 'primary_key':True, 'nullable':False},
		{'name': 'package_product_id', 'type_': UUID, 'nullable':False},
		{'name': 'product_id', 'type_': UUID, 'nullable':True},
		{'name': 'quantity', 'type_': Numeric, 'nullable': False, 'server_default': '1'},
		{'name': 'sale_ratio', 'type_': Numeric, 'nullable': False, 'server_default': '100'},
		{'name': 'created', 'type_': DateTime, 'nullable':True},
		{'name': 'modified', 'type_': DateTime, 'nullable':True},
		{'name': 'creator_id', 'type_': UUID, 'nullable':True},
		{'name': 'modifier_id', 'type_': UUID, 'nullable':True},
	],
})

data.append({
	'name':'product_specials',
	'columns': [
		{'name': 'id', 'type_': UUID, 'primary_key':True, 'nullable':False},
		{'name': 'product_id', 'type_': UUID, 'nullable':False},
		{'name': 'sale_price', 'type_': Numeric, 'nullable':False},
		{'name': 'begin', 'type_': Date, 'nullable':True},
		{'name': 'end', 'type_': Date, 'nullable':True},
		{'name': 'created', 'type_': DateTime, 'nullable':True},
		{'name': 'modified', 'type_': DateTime, 'nullable':True},
		{'name': 'creator_id', 'type_': UUID, 'nullable':True},
		{'name': 'modifier_id', 'type_': UUID, 'nullable':True},
	],
})

data.append({
	'name':'product_specials',
	'columns': [
		{'name': 'id', 'type_': UUID, 'primary_key':True, 'nullable':False},
		{'name': 'product_id', 'type_': UUID, 'nullable':False},
		{'name': 'first_sale', 'type_': Date, 'nullable':True},
		{'name': 'last_sale', 'type_': Date, 'nullable':True},
		{'name': 'created', 'type_': DateTime, 'nullable':True},
		{'name': 'modified', 'type_': DateTime, 'nullable':True},
		{'name': 'creator_id', 'type_': UUID, 'nullable':True},
		{'name': 'modifier_id', 'type_': UUID, 'nullable':True},
	],
})


def downgrade(migrate_engine):
	# Upgrade operations go here. Don't create your own engine; bind
	# migrate_engine to your metadata
	pass


def upgrade(migrate_engine):
	# Upgrade operations go here. Don't create your own engine; bind
	# migrate_engine to your metadata
	meta = MetaData(bind=migrate_engine, reflect=True)

	for tdata in data:
		if tdata['name'] not in meta:
			table = Table(tdata['name'], meta)
			table.create()
		else:
			table = meta.tables[tdata['name']]

		s = set()

		for cdata in tdata['columns']:
			s.add(cdata['name'])
			if cdata['name'] in table.columns:
				column = table.columns[cdata['name']]
				d = cdata.copy()
				del d['name']
				column.alter(**d)
			else:
				column = Column(**cdata)
				p = dict()
				if column.primary_key:
					p['primary_key_name'] = tdata['name'] + '_pkey'
				column.create(table, **p)
		for column in table.columns:
			if column.name not in s:
				logger.warning("Extra Column '%s' found in table '%s'", column.name, table.name)


#-- Table: bakedpotato.product_specials
#-- DROP TABLE bakedpotato.product_stats;

#CREATE TABLE bakedpotato.product_stats
#(
  #id uuid NOT NULL,
  #product_id uuid NOT NULL,
  #first_sale date,
  #last_sale date,
  #CONSTRAINT product_stats_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.product_stats
  #OWNER TO bakedpotato_owner;
#-- Table: bakedpotato.product_weekly_stats

#-- DROP TABLE bakedpotato.product_weekly_stats;

#CREATE TABLE bakedpotato.product_weekly_stats
#(
  #id uuid NOT NULL,
  #product_id uuid NOT NULL,
  #customer_order_quantity numeric DEFAULT 0,
  #customer_shipment_quantity numeric DEFAULT 0,
  #supplier_shipment_quantity numeric DEFAULT 0,
  #customer_order_total numeric DEFAULT 0,
  #iso_year integer,
  #iso_week integer,
  #customer_shipment_total numeric,
  #supplier_shipment_total numeric,
  #CONSTRAINT product_weekly_stats_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.product_weekly_stats
  #OWNER TO bakedpotato_owner;
#-- Table: bakedpotato.product_yearly_stats

#-- DROP TABLE bakedpotato.product_yearly_stats;

#CREATE TABLE bakedpotato.product_yearly_stats
#(
  #id uuid NOT NULL,
  #product_id uuid,
  #customer_order_quantity numeric,
  #customer_shipment_quantity numeric,
  #supplier_shipment_quantity numeric,
  #customer_order_total numeric,
  #customer_shipment_total numeric,
  #supplier_shipment_total numeric,
  #year integer,
  #CONSTRAINT product_yearly_stats_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.product_yearly_stats
  #OWNER TO bakedpotato_owner;
#-- Table: bakedpotato.products

#-- DROP TABLE bakedpotato.products;

#CREATE TABLE bakedpotato.products
#(
  #id uuid NOT NULL,
  #manufacturer_id uuid NOT NULL,
  #scale_id uuid,
  #identifier character varying(20) NOT NULL,
  #name character varying(255) DEFAULT NULL::character varying,
  #description character varying(255) DEFAULT NULL::character varying,
  #archived boolean NOT NULL DEFAULT false,
  #supplier_phased_out boolean NOT NULL DEFAULT false,
  #sort integer DEFAULT 0,
  #customer_order_item_count integer,
  #customer_shipment_item_count integer,
  #inventory_item_count integer,
  #supplier_catalog_item_count integer,
  #supplier_shipment_item_count integer,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #creator_id uuid,
  #modifier_id uuid,
  #legacy_flag integer,
  #image_url character varying(255) DEFAULT NULL::character varying,
  #url character varying(255) DEFAULT NULL::character varying,
  #cost numeric,
  #lock_cost boolean NOT NULL DEFAULT false,
  #retail numeric,
  #lock_retail boolean NOT NULL DEFAULT false,
  #sale numeric,
  #lock_sale boolean NOT NULL DEFAULT false,
  #enabled boolean NOT NULL DEFAULT true,
  #lock_category boolean NOT NULL DEFAULT false,
  #lock_name boolean NOT NULL DEFAULT false,
  #force_in_stock boolean NOT NULL DEFAULT false,
  #stock numeric NOT NULL DEFAULT 0,
  #shippable boolean NOT NULL DEFAULT true,
  #lock_scale boolean NOT NULL DEFAULT false,
  #category_id integer,
  #product_conversion_count integer,
  #product_package_count integer,
  #catalog_item_count integer,
  #supplier_catalog_item_id uuid,
  #serial integer,
  #supplier_stock boolean NOT NULL DEFAULT false,
  #supplier_advanced boolean NOT NULL DEFAULT false,
  #supplier_special boolean NOT NULL DEFAULT false,
  #ratio numeric NOT NULL DEFAULT 100,
  #base_sale numeric NOT NULL DEFAULT 0,
  #lock_base_sale boolean NOT NULL DEFAULT false,
  #CONSTRAINT products_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.products
  #OWNER TO bakedpotato_owner;

#-- Index: bakedpotato.products__identifier

#-- DROP INDEX bakedpotato.products__identifier;

#CREATE INDEX products__identifier
  #ON bakedpotato.products
  #USING btree
  #(identifier COLLATE pg_catalog."default" );

#-- Index: bakedpotato.products__manufacturer

#-- DROP INDEX bakedpotato.products__manufacturer;

#CREATE INDEX products__manufacturer
  #ON bakedpotato.products
  #USING btree
  #(manufacturer_id );

#-- Index: bakedpotato.products__unique

#-- DROP INDEX bakedpotato.products__unique;

#CREATE UNIQUE INDEX products__unique
  #ON bakedpotato.products
  #USING btree
  #(manufacturer_id , identifier COLLATE pg_catalog."default" );

#-- Table: bakedpotato.products_images

#-- DROP TABLE bakedpotato.products_images;

#CREATE TABLE bakedpotato.products_images
#(
  #id uuid NOT NULL,
  #product_id uuid NOT NULL,
  #image_id uuid NOT NULL,
  #CONSTRAINT products_images_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.products_images
  #OWNER TO bakedpotato_owner;

#-- Index: bakedpotato.products_images_idx1

#-- DROP INDEX bakedpotato.products_images_idx1;

#CREATE UNIQUE INDEX products_images_idx1
  #ON bakedpotato.products_images
  #USING btree
  #(product_id , image_id );

#-- Table: bakedpotato.scale_conversions

#-- DROP TABLE bakedpotato.scale_conversions;

#CREATE TABLE bakedpotato.scale_conversions
#(
  #id uuid NOT NULL,
  #scale_identifier character varying(255) NOT NULL,
  #scale_id uuid,
  #lock boolean NOT NULL DEFAULT false,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #creator_id uuid,
  #modifier_id uuid,
  #supplier_id uuid,
  #CONSTRAINT scale_conversions_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.scale_conversions
  #OWNER TO bakedpotato_owner;
#-- Table: bakedpotato.scales

#-- DROP TABLE bakedpotato.scales;

#CREATE TABLE bakedpotato.scales
#(
  #id uuid NOT NULL,
  #name character varying(255) NOT NULL,
  #ratio character varying(255) DEFAULT NULL::character varying,
  #gauge character varying(255) DEFAULT NULL::character varying,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #creator_id uuid,
  #modifier_id uuid,
  #enabled boolean NOT NULL DEFAULT false,
  #product_count integer,
  #scale_conversion_count integer,
  #supplier_catalog_item_count integer,
  #catalog_category_count integer,
  #serial integer,
  #CONSTRAINT scales_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.scales
  #OWNER TO bakedpotato_owner;
#-- Table: bakedpotato.settings

#-- DROP TABLE bakedpotato.settings;

#CREATE TABLE bakedpotato.settings
#(
  #id uuid NOT NULL,
  #class character varying(255) NOT NULL,
  #name character varying(255) NOT NULL,
  #value character varying(255) DEFAULT NULL::character varying,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #creator_id uuid,
  #modifier_id uuid,
  #CONSTRAINT settings_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.settings
  #OWNER TO bakedpotato_owner;
#-- Table: bakedpotato.shippers

#-- DROP TABLE bakedpotato.shippers;

#CREATE TABLE bakedpotato.shippers
#(
  #id uuid NOT NULL,
  #name character varying(255) DEFAULT NULL::character varying,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #creator_id uuid,
  #modifier_id uuid,
  #serial integer,
  #CONSTRAINT shippers_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.shippers
  #OWNER TO bakedpotato_owner;
#-- Table: bakedpotato.supplier_catalog_filters

#-- DROP TABLE bakedpotato.supplier_catalog_filters;

#CREATE TABLE bakedpotato.supplier_catalog_filters
#(
  #id uuid NOT NULL,
  #supplier_id uuid,
  #name character varying,
  #ghost_stock boolean,
  #ghost_phased_out boolean,
  #ghost_advanced boolean NOT NULL DEFAULT true,
  #version_model character varying,
  #opaque boolean NOT NULL DEFAULT true,
  #CONSTRAINT supplier_catalog_filters_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.supplier_catalog_filters
  #OWNER TO bakedpotato_owner;
#-- Table: bakedpotato.supplier_catalog_item_bowser_versions

#-- DROP TABLE bakedpotato.supplier_catalog_item_bowser_versions;

#CREATE TABLE bakedpotato.supplier_catalog_item_bowser_versions
#(
  #id uuid NOT NULL,
  #supplier_catalog_id uuid,
  #row_number integer,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #supplier_catalog_item_field_id uuid,
  #ghost boolean NOT NULL,
  #supplier_catalog_filter_id uuid,
  #effective timestamp without time zone,
  #CONSTRAINT supplier_catalog_item_bowser_versions_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.supplier_catalog_item_bowser_versions
  #OWNER TO postgres;

#-- Index: bakedpotato.supplier_catalog_item_bowser__supplier_catalog_id_row_numbe_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_bowser__supplier_catalog_id_row_numbe_idx;

#CREATE UNIQUE INDEX supplier_catalog_item_bowser__supplier_catalog_id_row_numbe_idx
  #ON bakedpotato.supplier_catalog_item_bowser_versions
  #USING btree
  #(supplier_catalog_id , row_number );

#-- Index: bakedpotato.supplier_catalog_item_bowser__supplier_catalog_item_field_i_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_bowser__supplier_catalog_item_field_i_idx;

#CREATE INDEX supplier_catalog_item_bowser__supplier_catalog_item_field_i_idx
  #ON bakedpotato.supplier_catalog_item_bowser_versions
  #USING btree
  #(supplier_catalog_item_field_id );

#-- Index: bakedpotato.supplier_catalog_item_bowser_versions_effective_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_bowser_versions_effective_idx;

#CREATE INDEX supplier_catalog_item_bowser_versions_effective_idx
  #ON bakedpotato.supplier_catalog_item_bowser_versions
  #USING btree
  #(effective  DESC NULLS LAST);

#-- Index: bakedpotato.supplier_catalog_item_bowser_versions_row_number_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_bowser_versions_row_number_idx;

#CREATE INDEX supplier_catalog_item_bowser_versions_row_number_idx
  #ON bakedpotato.supplier_catalog_item_bowser_versions
  #USING btree
  #(row_number );

#-- Index: bakedpotato.supplier_catalog_item_bowser_versions_supplier_catalog_id_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_bowser_versions_supplier_catalog_id_idx;

#CREATE INDEX supplier_catalog_item_bowser_versions_supplier_catalog_id_idx
  #ON bakedpotato.supplier_catalog_item_bowser_versions
  #USING btree
  #(supplier_catalog_id );

#-- Table: bakedpotato.supplier_catalog_item_emery_versions

#-- DROP TABLE bakedpotato.supplier_catalog_item_emery_versions;

#CREATE TABLE bakedpotato.supplier_catalog_item_emery_versions
#(
  #id uuid NOT NULL,
  #supplier_catalog_id uuid,
  #row_number integer,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #supplier_catalog_item_field_id uuid,
  #ghost boolean NOT NULL,
  #supplier_catalog_filter_id uuid,
  #effective timestamp without time zone,
  #CONSTRAINT supplier_catalog_item_emery_versions_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.supplier_catalog_item_emery_versions
  #OWNER TO postgres;

#-- Index: bakedpotato.supplier_catalog_item_emery_v_supplier_catalog_id_row_numbe_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_emery_v_supplier_catalog_id_row_numbe_idx;

#CREATE UNIQUE INDEX supplier_catalog_item_emery_v_supplier_catalog_id_row_numbe_idx
  #ON bakedpotato.supplier_catalog_item_emery_versions
  #USING btree
  #(supplier_catalog_id , row_number );

#-- Index: bakedpotato.supplier_catalog_item_emery_v_supplier_catalog_item_field_i_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_emery_v_supplier_catalog_item_field_i_idx;

#CREATE INDEX supplier_catalog_item_emery_v_supplier_catalog_item_field_i_idx
  #ON bakedpotato.supplier_catalog_item_emery_versions
  #USING btree
  #(supplier_catalog_item_field_id );

#-- Index: bakedpotato.supplier_catalog_item_emery_versions_row_number_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_emery_versions_row_number_idx;

#CREATE INDEX supplier_catalog_item_emery_versions_row_number_idx
  #ON bakedpotato.supplier_catalog_item_emery_versions
  #USING btree
  #(row_number );

#-- Index: bakedpotato.supplier_catalog_item_emery_versions_supplier_catalog_id_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_emery_versions_supplier_catalog_id_idx;

#CREATE INDEX supplier_catalog_item_emery_versions_supplier_catalog_id_idx
  #ON bakedpotato.supplier_catalog_item_emery_versions
  #USING btree
  #(supplier_catalog_id );

#-- Table: bakedpotato.supplier_catalog_item_exactrail_versions

#-- DROP TABLE bakedpotato.supplier_catalog_item_exactrail_versions;

#CREATE TABLE bakedpotato.supplier_catalog_item_exactrail_versions
#(
  #id uuid NOT NULL,
  #supplier_catalog_id uuid,
  #row_number integer,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #supplier_catalog_item_field_id uuid,
  #ghost boolean NOT NULL,
  #supplier_catalog_filter_id uuid,
  #effective timestamp without time zone,
  #CONSTRAINT supplier_catalog_item_exactrail_versions_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.supplier_catalog_item_exactrail_versions
  #OWNER TO postgres;

#-- Index: bakedpotato.supplier_catalog_item_exactra_supplier_catalog_id_row_numbe_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_exactra_supplier_catalog_id_row_numbe_idx;

#CREATE UNIQUE INDEX supplier_catalog_item_exactra_supplier_catalog_id_row_numbe_idx
  #ON bakedpotato.supplier_catalog_item_exactrail_versions
  #USING btree
  #(supplier_catalog_id , row_number );

#-- Index: bakedpotato.supplier_catalog_item_exactra_supplier_catalog_item_field_i_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_exactra_supplier_catalog_item_field_i_idx;

#CREATE INDEX supplier_catalog_item_exactra_supplier_catalog_item_field_i_idx
  #ON bakedpotato.supplier_catalog_item_exactrail_versions
  #USING btree
  #(supplier_catalog_item_field_id );

#-- Index: bakedpotato.supplier_catalog_item_exactrail_version_supplier_catalog_id_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_exactrail_version_supplier_catalog_id_idx;

#CREATE INDEX supplier_catalog_item_exactrail_version_supplier_catalog_id_idx
  #ON bakedpotato.supplier_catalog_item_exactrail_versions
  #USING btree
  #(supplier_catalog_id );

#-- Index: bakedpotato.supplier_catalog_item_exactrail_versions_row_number_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_exactrail_versions_row_number_idx;

#CREATE INDEX supplier_catalog_item_exactrail_versions_row_number_idx
  #ON bakedpotato.supplier_catalog_item_exactrail_versions
  #USING btree
  #(row_number );

#-- Table: bakedpotato.supplier_catalog_item_fields

#-- DROP TABLE bakedpotato.supplier_catalog_item_fields;

#CREATE TABLE bakedpotato.supplier_catalog_item_fields
#(
  #id uuid NOT NULL,
  #fields bytea NOT NULL,
  #checksum character(40) NOT NULL,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #supplier_catalog_item_version_count integer,
  #name character varying,
  #product_identifier character varying,
  #manufacturer_identifier character varying,
  #cost numeric,
  #retail numeric,
  #stock boolean,
  #scale_identifier character varying,
  #category_identifier character varying,
  #phased_out boolean,
  #special boolean,
  #special_cost numeric,
  #advanced boolean,
  #supplier_id uuid,
  #available date,
  #supplier_catalog_filter_id uuid,
  #compressed boolean,
  #ghost boolean NOT NULL DEFAULT false,
  #CONSTRAINT supplier_catalog_item_fields_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.supplier_catalog_item_fields
  #OWNER TO bakedpotato_owner;

#-- Index: bakedpotato.supplier_catalog_item_fields__checksum

#-- DROP INDEX bakedpotato.supplier_catalog_item_fields__checksum;

#CREATE INDEX supplier_catalog_item_fields__checksum
  #ON bakedpotato.supplier_catalog_item_fields
  #USING btree
  #(checksum COLLATE pg_catalog."default" );

#-- Index: bakedpotato.supplier_catalog_item_fields__manufacturer

#-- DROP INDEX bakedpotato.supplier_catalog_item_fields__manufacturer;

#CREATE INDEX supplier_catalog_item_fields__manufacturer
  #ON bakedpotato.supplier_catalog_item_fields
  #USING btree
  #(manufacturer_identifier COLLATE pg_catalog."default" );

#-- Index: bakedpotato.supplier_catalog_item_fields__product

#-- DROP INDEX bakedpotato.supplier_catalog_item_fields__product;

#CREATE INDEX supplier_catalog_item_fields__product
  #ON bakedpotato.supplier_catalog_item_fields
  #USING btree
  #(product_identifier COLLATE pg_catalog."default" );

#-- Index: bakedpotato.supplier_catalog_item_fields__supplier

#-- DROP INDEX bakedpotato.supplier_catalog_item_fields__supplier;

#CREATE INDEX supplier_catalog_item_fields__supplier
  #ON bakedpotato.supplier_catalog_item_fields
  #USING btree
  #(supplier_id );

#-- Index: bakedpotato.supplier_catalog_item_fields_supplier_id_manufacturer_ident_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_fields_supplier_id_manufacturer_ident_idx;

#CREATE INDEX supplier_catalog_item_fields_supplier_id_manufacturer_ident_idx
  #ON bakedpotato.supplier_catalog_item_fields
  #USING btree
  #(supplier_id , manufacturer_identifier COLLATE pg_catalog."default" , product_identifier COLLATE pg_catalog."default" );

#-- Table: bakedpotato.supplier_catalog_item_heartland_versions

#-- DROP TABLE bakedpotato.supplier_catalog_item_heartland_versions;

#CREATE TABLE bakedpotato.supplier_catalog_item_heartland_versions
#(
  #id uuid NOT NULL,
  #supplier_catalog_id uuid,
  #row_number integer,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #supplier_catalog_item_field_id uuid,
  #ghost boolean NOT NULL,
  #supplier_catalog_filter_id uuid,
  #effective timestamp without time zone,
  #CONSTRAINT supplier_catalog_item_heartland_versions_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.supplier_catalog_item_heartland_versions
  #OWNER TO postgres;

#-- Index: bakedpotato.supplier_catalog_item_heartla_supplier_catalog_id_row_numbe_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_heartla_supplier_catalog_id_row_numbe_idx;

#CREATE UNIQUE INDEX supplier_catalog_item_heartla_supplier_catalog_id_row_numbe_idx
  #ON bakedpotato.supplier_catalog_item_heartland_versions
  #USING btree
  #(supplier_catalog_id , row_number );

#-- Index: bakedpotato.supplier_catalog_item_heartla_supplier_catalog_item_field_i_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_heartla_supplier_catalog_item_field_i_idx;

#CREATE INDEX supplier_catalog_item_heartla_supplier_catalog_item_field_i_idx
  #ON bakedpotato.supplier_catalog_item_heartland_versions
  #USING btree
  #(supplier_catalog_item_field_id );

#-- Index: bakedpotato.supplier_catalog_item_heartland_version_supplier_catalog_id_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_heartland_version_supplier_catalog_id_idx;

#CREATE INDEX supplier_catalog_item_heartland_version_supplier_catalog_id_idx
  #ON bakedpotato.supplier_catalog_item_heartland_versions
  #USING btree
  #(supplier_catalog_id );

#-- Index: bakedpotato.supplier_catalog_item_heartland_versions_row_number_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_heartland_versions_row_number_idx;

#CREATE INDEX supplier_catalog_item_heartland_versions_row_number_idx
  #ON bakedpotato.supplier_catalog_item_heartland_versions
  #USING btree
  #(row_number );

#-- Table: bakedpotato.supplier_catalog_item_versions

#-- DROP TABLE bakedpotato.supplier_catalog_item_versions;

#CREATE TABLE bakedpotato.supplier_catalog_item_versions
#(
  #id uuid NOT NULL,
  #supplier_catalog_id uuid,
  #row_number integer,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #supplier_catalog_item_field_id uuid,
  #ghost boolean NOT NULL,
  #supplier_catalog_filter_id uuid,
  #next_supplier_catalog_id uuid,
  #prev_supplier_catalog_id uuid,
  #next_supplier_catalog_item_version_id uuid,
  #prev_supplier_catalog_item_version_id uuid,
  #effective timestamp without time zone,
  #CONSTRAINT supplier_catalog_item_versions_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.supplier_catalog_item_versions
  #OWNER TO bakedpotato_owner;

#-- Index: bakedpotato.supplier_catalog_item_versions__catalog

#-- DROP INDEX bakedpotato.supplier_catalog_item_versions__catalog;

#CREATE INDEX supplier_catalog_item_versions__catalog
  #ON bakedpotato.supplier_catalog_item_versions
  #USING btree
  #(supplier_catalog_id );

#-- Index: bakedpotato."supplier_catalog_item_versions__catalog+row"

#-- DROP INDEX bakedpotato."supplier_catalog_item_versions__catalog+row";

#CREATE UNIQUE INDEX "supplier_catalog_item_versions__catalog+row"
  #ON bakedpotato.supplier_catalog_item_versions
  #USING btree
  #(supplier_catalog_id , row_number );
#ALTER TABLE bakedpotato.supplier_catalog_item_versions CLUSTER ON "supplier_catalog_item_versions__catalog+row";

#-- Index: bakedpotato.supplier_catalog_item_versions__field

#-- DROP INDEX bakedpotato.supplier_catalog_item_versions__field;

#CREATE INDEX supplier_catalog_item_versions__field
  #ON bakedpotato.supplier_catalog_item_versions
  #USING btree
  #(supplier_catalog_item_field_id );

#-- Index: bakedpotato.supplier_catalog_item_versions__row

#-- DROP INDEX bakedpotato.supplier_catalog_item_versions__row;

#CREATE INDEX supplier_catalog_item_versions__row
  #ON bakedpotato.supplier_catalog_item_versions
  #USING btree
  #(row_number );

#-- Table: bakedpotato.supplier_catalog_item_walthers_versions

#-- DROP TABLE bakedpotato.supplier_catalog_item_walthers_versions;

#CREATE TABLE bakedpotato.supplier_catalog_item_walthers_versions
#(
  #id uuid NOT NULL,
  #supplier_catalog_id uuid,
  #row_number integer,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #supplier_catalog_item_field_id uuid,
  #supplier_catalog_filter_id uuid,
  #effective timestamp without time zone,
  #CONSTRAINT supplier_catalog_item_walthers_versions_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.supplier_catalog_item_walthers_versions
  #OWNER TO postgres;

#-- Index: bakedpotato.supplier_catalog_item_walther_supplier_catalog_id_row_numbe_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_walther_supplier_catalog_id_row_numbe_idx;

#CREATE UNIQUE INDEX supplier_catalog_item_walther_supplier_catalog_id_row_numbe_idx
  #ON bakedpotato.supplier_catalog_item_walthers_versions
  #USING btree
  #(supplier_catalog_id , row_number );

#-- Index: bakedpotato.supplier_catalog_item_walther_supplier_catalog_item_field_i_idx

#-- DROP INDEX bakedpotato.supplier_catalog_item_walther_supplier_catalog_item_field_i_idx;

#CREATE INDEX supplier_catalog_item_walther_supplier_catalog_item_field_i_idx
  #ON bakedpotato.supplier_catalog_item_walthers_versions
  #USING btree
  #(supplier_catalog_item_field_id );

#-- Table: bakedpotato.supplier_catalog_items

#-- DROP TABLE bakedpotato.supplier_catalog_items;

#CREATE TABLE bakedpotato.supplier_catalog_items
#(
  #id uuid NOT NULL,
  #supplier_id uuid NOT NULL,
  #manufacturer_id uuid,
  #product_id uuid,
  #name character varying(1024) DEFAULT NULL::character varying,
  #in_stock boolean NOT NULL DEFAULT false,
  #phased_out boolean NOT NULL DEFAULT false,
  #advanced boolean NOT NULL DEFAULT false,
  #available date,
  #special boolean NOT NULL DEFAULT false,
  #retail numeric NOT NULL DEFAULT 0.0,
  #cost numeric NOT NULL DEFAULT 0.0,
  #sale numeric NOT NULL DEFAULT 0.0,
  #scale_identifier character varying(255) DEFAULT NULL::character varying,
  #category_identifier character varying(255) DEFAULT NULL::character varying,
  #rank integer DEFAULT 0,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #creator_id uuid,
  #modifier_id uuid,
  #legacy_flag integer NOT NULL DEFAULT 0,
  #special_cost double precision NOT NULL DEFAULT 0.0,
  #count integer,
  #price_control_id uuid,
  #minimum_advertised_sale numeric,
  #special_minimum_advertised_sale numeric,
  #manufacturer_identifier character varying(255) NOT NULL,
  #product_identifier character varying(255) NOT NULL,
  #effective timestamp without time zone,
  #quantity numeric NOT NULL DEFAULT 1,
  #scale_id uuid,
  #category_id integer,
  #quantity_cost numeric NOT NULL DEFAULT 0.0,
  #quantity_retail numeric NOT NULL DEFAULT 0.0,
  #quantity_special_cost numeric NOT NULL DEFAULT 0.0,
  #serial integer,
  #CONSTRAINT supplier_catalog_items_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.supplier_catalog_items
  #OWNER TO bakedpotato_owner;

#-- Index: bakedpotato.supplier_catalog_items__product

#-- DROP INDEX bakedpotato.supplier_catalog_items__product;

#CREATE INDEX supplier_catalog_items__product
  #ON bakedpotato.supplier_catalog_items
  #USING btree
  #(product_id );

#-- Index: bakedpotato.supplier_catalog_items__unique

#-- DROP INDEX bakedpotato.supplier_catalog_items__unique;

#CREATE UNIQUE INDEX supplier_catalog_items__unique
  #ON bakedpotato.supplier_catalog_items
  #USING btree
  #(supplier_id , manufacturer_identifier COLLATE pg_catalog."default" , product_identifier COLLATE pg_catalog."default" );

#-- Table: bakedpotato.supplier_catalog_stats

#-- DROP TABLE bakedpotato.supplier_catalog_stats;

#CREATE TABLE bakedpotato.supplier_catalog_stats
#(
  #id uuid NOT NULL,
  #manufacturer_id uuid,
  #supplier_id uuid,
  #count integer,
  #avg_retail numeric,
  #stddev_retail numeric,
  #avg_cost numeric,
  #stddev_cost numeric,
  #avg_ratio numeric,
  #stddev_ratio numeric,
  #CONSTRAINT supplier_catalog_stats_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.supplier_catalog_stats
  #OWNER TO bakedpotato_owner;
#-- Table: bakedpotato.supplier_catalogs

#-- DROP TABLE bakedpotato.supplier_catalogs;

#CREATE TABLE bakedpotato.supplier_catalogs
#(
  #id uuid NOT NULL,
  #issue_date timestamp without time zone,
  #file_import_id uuid,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #creator_id uuid,
  #modifier_id uuid,
  #supplier_catalog_field_count integer,
  #supplier_id uuid,
  #supplier_catalog_item_version_count integer,
  #lock_issue_date boolean NOT NULL DEFAULT false,
  #supplier_catalog_filter_id uuid,
  #next_supplier_catalog_id uuid,
  #prev_supplier_catalog_id uuid,
  #item_versions_loaded boolean NOT NULL DEFAULT false,
  #CONSTRAINT supplier_catalogs_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.supplier_catalogs
  #OWNER TO bakedpotato_owner;

#-- Index: bakedpotato.supplier_catalogs__file

#-- DROP INDEX bakedpotato.supplier_catalogs__file;

#CREATE INDEX supplier_catalogs__file
  #ON bakedpotato.supplier_catalogs
  #USING btree
  #(file_import_id );

#-- Index: bakedpotato.supplier_catalogs__issue_date

#-- DROP INDEX bakedpotato.supplier_catalogs__issue_date;

#CREATE INDEX supplier_catalogs__issue_date
  #ON bakedpotato.supplier_catalogs
  #USING btree
  #(issue_date );

#-- Index: bakedpotato.supplier_catalogs__supplier

#-- DROP INDEX bakedpotato.supplier_catalogs__supplier;

#CREATE INDEX supplier_catalogs__supplier
  #ON bakedpotato.supplier_catalogs
  #USING btree
  #(supplier_id );

#-- Table: bakedpotato.supplier_shipment_items

#-- DROP TABLE bakedpotato.supplier_shipment_items;

#CREATE TABLE bakedpotato.supplier_shipment_items
#(
  #id uuid NOT NULL,
  #supplier_shipment_id uuid,
  #quantity numeric,
  #cost numeric,
  #discrepancy numeric,
  #product_id uuid,
  #supplier_order_item_id uuid,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #creator_id uuid,
  #modifier_id uuid,
  #serial integer,
  #CONSTRAINT supplier_shipment_items_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.supplier_shipment_items
  #OWNER TO bakedpotato_owner;
#-- Table: bakedpotato.supplier_shipments

#-- DROP TABLE bakedpotato.supplier_shipments;

#CREATE TABLE bakedpotato.supplier_shipments
#(
  #id uuid NOT NULL,
  #warehouse_id uuid,
  #shipped date,
  #received date,
  #supplier_id uuid,
  #identifier character varying(255) DEFAULT NULL::character varying,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #creator_id uuid,
  #modifier_id uuid,
  #postage numeric,
  #serial integer,
  #CONSTRAINT supplier_shipments_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.supplier_shipments
  #OWNER TO bakedpotato_owner;
#-- Table: bakedpotato.supplier_special_filters

#-- DROP TABLE bakedpotato.supplier_special_filters;

#CREATE TABLE bakedpotato.supplier_special_filters
#(
  #id uuid NOT NULL,
  #name character varying,
  #supplier_id uuid,
  #CONSTRAINT supplier_special_filters_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.supplier_special_filters
  #OWNER TO bakedpotato_owner;
#-- Table: bakedpotato.supplier_special_item_fields

#-- DROP TABLE bakedpotato.supplier_special_item_fields;

#CREATE TABLE bakedpotato.supplier_special_item_fields
#(
  #id uuid NOT NULL,
  #fields bytea,
  #checksum character(40),
  #supplier_special_filter_id uuid,
  #compressed boolean,
  #supplier_id uuid,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #manufacturer_identifier character varying,
  #product_identifier character varying,
  #special_cost numeric,
  #CONSTRAINT supplier_special_item_fields_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.supplier_special_item_fields
  #OWNER TO bakedpotato_owner;
#-- Table: bakedpotato.supplier_special_item_versions

#-- DROP TABLE bakedpotato.supplier_special_item_versions;

#CREATE TABLE bakedpotato.supplier_special_item_versions
#(
  #id uuid NOT NULL,
  #supplier_special_id uuid,
  #supplier_special_item_field_id uuid,
  #row_number integer,
  #ghost boolean,
  #CONSTRAINT supplier_special_item_versions_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.supplier_special_item_versions
  #OWNER TO bakedpotato_owner;

#-- Index: bakedpotato.supplier_special_item_versions__supplier_special

#-- DROP INDEX bakedpotato.supplier_special_item_versions__supplier_special;

#CREATE INDEX supplier_special_item_versions__supplier_special
  #ON bakedpotato.supplier_special_item_versions
  #USING btree
  #(supplier_special_id );

#-- Index: bakedpotato.supplier_special_item_versions__supplier_special_item_field

#-- DROP INDEX bakedpotato.supplier_special_item_versions__supplier_special_item_field;

#CREATE INDEX supplier_special_item_versions__supplier_special_item_field
  #ON bakedpotato.supplier_special_item_versions
  #USING btree
  #(supplier_special_item_field_id );

#-- Index: bakedpotato.supplier_special_item_versions__unique

#-- DROP INDEX bakedpotato.supplier_special_item_versions__unique;

#CREATE UNIQUE INDEX supplier_special_item_versions__unique
  #ON bakedpotato.supplier_special_item_versions
  #USING btree
  #(supplier_special_id , row_number );


#-- Table: bakedpotato.supplier_special_items

#-- DROP TABLE bakedpotato.supplier_special_items;

#CREATE TABLE bakedpotato.supplier_special_items
#(
  #id uuid NOT NULL,
  #CONSTRAINT supplier_special_items_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.supplier_special_items
  #OWNER TO bakedpotato_owner;
#-- Table: bakedpotato.supplier_specials

#-- DROP TABLE bakedpotato.supplier_specials;

#CREATE TABLE bakedpotato.supplier_specials
#(
  #id uuid NOT NULL,
  #file_import_id uuid,
  #begin_date date,
  #end_date date,
  #supplier_id uuid,
  #supplier_special_filter_id uuid,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #CONSTRAINT supplier_specials_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.supplier_specials
  #OWNER TO bakedpotato_owner;
#-- Table: bakedpotato.suppliers

#-- DROP TABLE bakedpotato.suppliers;

#CREATE TABLE bakedpotato.suppliers
#(
  #id uuid NOT NULL,
  #name character varying(255) NOT NULL,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #identifier integer,
  #creator_id uuid,
  #modifier_id uuid,
  #catalog_item_count integer,
  #category_conversion_count integer,
  #serial integer,
  #CONSTRAINT suppliers_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.suppliers
  #OWNER TO bakedpotato_owner;
#-- Table: bakedpotato.users

#-- DROP TABLE bakedpotato.users;

#CREATE TABLE bakedpotato.users
#(
  #id uuid NOT NULL,
  #username character varying(255) DEFAULT NULL::character varying,
  #password character varying(255) DEFAULT NULL::character varying,
  #group_id uuid,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #name character varying(255) DEFAULT NULL::character varying,
  #warehouse_id uuid,
  #creator_id uuid,
  #modifier_id uuid,
  #serial integer,
  #CONSTRAINT users_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.users
  #OWNER TO bakedpotato_owner;
#-- Table: bakedpotato.uuid_conversions

#-- DROP TABLE bakedpotato.uuid_conversions;

#CREATE TABLE bakedpotato.uuid_conversions
#(
  #id uuid NOT NULL,
  #table_name character varying NOT NULL,
  #old_id integer NOT NULL,
  #CONSTRAINT uuid_conversions_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.uuid_conversions
  #OWNER TO bakedpotato_owner;

#-- Index: bakedpotato.uuid_conversions_table_name_old_id_idx

#-- DROP INDEX bakedpotato.uuid_conversions_table_name_old_id_idx;

#CREATE UNIQUE INDEX uuid_conversions_table_name_old_id_idx
  #ON bakedpotato.uuid_conversions
  #USING btree
  #(table_name COLLATE pg_catalog."default" , old_id );

#-- Table: bakedpotato.warehouses

#-- DROP TABLE bakedpotato.warehouses;

#CREATE TABLE bakedpotato.warehouses
#(
  #id uuid NOT NULL,
  #name character varying(255) NOT NULL,
  #created timestamp without time zone,
  #modified timestamp without time zone,
  #creator_id uuid,
  #modifier_id uuid,
  #customer_order_count integer,
  #customer_shipment_count integer,
  #supplier_shipment_count integer,
  #inventory_audit_count integer,
  #serial integer,
  #CONSTRAINT warehouses_pkey PRIMARY KEY (id )
#)
#WITH (
  #OIDS=FALSE
#);
#ALTER TABLE bakedpotato.warehouses
  #OWNER TO bakedpotato_owner;
