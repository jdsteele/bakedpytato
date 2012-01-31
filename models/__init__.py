models = dict()
from barcode_conversion import BarcodeConversion
models['BarcodeConversion'] = BarcodeConversion
from catalog_item import CatalogItem
models['CatalogItem'] = CatalogItem
from category_conversion import CategoryConversion
models['CategoryConversion'] = CategoryConversion
from customer_incidental import CustomerIncidental
models['CustomerIncidental'] = CustomerIncidental
from customer_order import CustomerOrder
models['CustomerOrder'] = CustomerOrder
from customer_order_incidental import CustomerOrderIncidental
models['CustomerOrderIncidental'] = CustomerOrderIncidental
from customer_order_item import CustomerOrderItem
models['CustomerOrderItem'] = CustomerOrderItem
from customer_shipment_item import CustomerShipmentItem
models['CustomerShipmentItem'] = CustomerShipmentItem
from inventory_audit import InventoryAudit
models['InventoryAudit'] = InventoryAudit
from inventory_audit_item import InventoryAuditItem
models['InventoryAuditItem'] = InventoryAuditItem
from inventory_item import InventoryItem
models['InventoryItem'] = InventoryItem
from manufacturer import Manufacturer
models['Manufacturer'] = Manufacturer
from manufacturer_conversion import ManufacturerConversion
models['ManufacturerConversion'] = ManufacturerConversion
from price_control import PriceControl
models['PriceControl'] = PriceControl
from product import Product
models['Product'] = Product
from product_barcode import ProductBarcode
models['ProductBarcode'] = ProductBarcode
from product_conversion import ProductConversion
models['ProductConversion'] = ProductConversion
from scale import Scale
models['Scale'] = Scale
from scale_conversion import ScaleConversion
models['ScaleConversion'] = ScaleConversion
from supplier import Supplier
models['Supplier'] = Supplier
from supplier_catalog import SupplierCatalog
models['SupplierCatalog'] = SupplierCatalog
from supplier_catalog_item import SupplierCatalogItem
models['SupplierCatalogItem'] = SupplierCatalogItem
from supplier_catalog_item_field import SupplierCatalogItemField
models['SupplierCatalogItemField'] = SupplierCatalogItemField
from supplier_catalog_item_version import SupplierCatalogItemVersion
models['SupplierCatalogItemVersion'] = SupplierCatalogItemVersion

