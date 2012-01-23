from category_conversion import CategoryConversion
from customer_incidental import CustomerIncidental
from customer_order import CustomerOrder
from customer_order_incidental import CustomerOrderIncidental
from customer_order_item import CustomerOrderItem
from customer_shipment_item import CustomerShipmentItem
from inventory_item import InventoryItem
from manufacturer import Manufacturer
from manufacturer_conversion import ManufacturerConversion
from price_control import PriceControl
from product import Product
from product_conversion import ProductConversion
from scale import Scale
from scale_conversion import ScaleConversion
from supplier import Supplier
from supplier_catalog import SupplierCatalog
from supplier_catalog_item import SupplierCatalogItem
from supplier_catalog_item_field import SupplierCatalogItemField
from supplier_catalog_item_version import SupplierCatalogItemVersion

models = dict()
models['CategoryConversion'] = CategoryConversion
models['CustomerIncidental'] = CustomerIncidental
models['CustomerOrder'] = CustomerOrder
models['CustomerOrderIncidental'] = CustomerOrderIncidental
models['CustomerOrderItem'] = CustomerOrderItem
models['InventoryItem'] = InventoryItem
models['Manufacturer'] = Manufacturer
models['ManufacturerConversion'] = ManufacturerConversion
models['PriceControl'] = PriceControl
models['Product'] = Product
models['ProductConversion'] = ProductConversion
models['Scale'] = Scale
models['ScaleConversion'] = ScaleConversion
models['Supplier'] = Supplier
models['SupplierCatalog'] = SupplierCatalog
models['SupplierCatalogItem'] = SupplierCatalogItem
models['SupplierCatalogItemField'] = SupplierCatalogItemField
models['SupplierCatalogItemVersion'] = SupplierCatalogItemVersion
#models[''] = 

