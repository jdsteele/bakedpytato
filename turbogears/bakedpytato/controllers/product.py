# -*- coding: utf-8 -*-
"""Product controller module"""

# turbogears imports
from tg import expose
#from tg import redirect, validate, flash

# third party imports
#from pylons.i18n import ugettext as _
#from repoze.what import predicates

# project specific imports
from bakedpytato.lib.base import BaseController
from bakedpytato.model import DBSession, metadata
from bakedpytato.model import ProductModel, ManufacturerModel
from bakedpytato.lib.data_grid import SortableDataGrid, SortableColumn

from tg.decorators import paginate
from tg import tmpl_context
from bakedpytato.widgets.product_search_form import product_search_form

from sqlalchemy import asc, desc
import genshi


product_grid = SortableDataGrid(fields=[
	SortableColumn('Manufacturer', 'manufacturer.name', ProductModel.sort),
	SortableColumn('Identifier', 'identifier', ProductModel.sort),
])


class ProductController(BaseController):
	#Uncomment this line if your controller requires an authenticated user
	#allow_only = authorize.not_anonymous()


	@expose('bakedpytato.templates.product__index')
	def index(self):
		return dict(page='index')


	@expose('bakedpytato.templates.search_form')
	def search(self, *args, **kw):
		tmpl_context.form = product_search_form
		return dict(modelname='Product', value=kw)


	@expose('bakedpytato.templates.page')
	@paginate("data", items_per_page=20)
	def page(self, *args, **kw):
		data = DBSession.query(ProductModel)

		identifier = kw.get('identifier')
		if identifier:
			data = data.filter(ProductModel.identifier == identifier)

		sort_col_name = kw.get('sort_col')
		sort_col = product_grid.find_col(sort_col_name)
		if sort_col:
			sort_dir = kw.get('sort_dir')
			if sort_dir == 'asc':
				data = data.order_by(asc(sort_col.sa_col))
			elif sort_dir == 'desc':
				data = data.order_by(desc(sort_col.sa_col))
			
		
		return dict(page='page', grid=product_grid, data=data)
