# -*- coding: utf-8 -*-
"""
	BakedPotato — Inventory Management System

	BakedPotato IMS
	Copyright 2010-2012, John David Steele (john.david.steele@gmail.com)

	Licensed under The MIT License
	Redistributions of files must retain the above copyright notice.

	@copyright	 Copyright 2010-2012, John David Steele (john.david.steele@gmail.com)
	@license	   MIT License (http://www.opensource.org/licenses/mit-license.php)
"""
### Pragma
from __future__ import unicode_literals

### Standard Library
import hashlib
import json
import logging

### Extended Library

#### Genshi
import genshi

#### Pylons
#from pylons.i18n import ugettext as _

#### Repoze
#from repoze.what import predicates

#### SqlAlchemy
from sqlalchemy import asc, desc, or_

#### ToscaWidgets
from tw.api import js_callback
from tw.forms import SingleSelectField
from tw.jquery import FlexiGrid

#### TurboGears
from tg import expose, redirect, validate, flash
from tg import tmpl_context, session
from tg import request
from tg.decorators import paginate


### Application Library
from bakedpytato.lib.base import BaseController
from bakedpytato.lib.param_filter import ParamFilter
from bakedpytato.lib import validators


from bakedpytato.model import DBSession, metadata
from bakedpytato.model import ProductModel, ManufacturerModel
#from bakedpytato.lib.data_grid import SortableDataGrid, SortableColumn
#from bakedpytato.widgets.product_search_form import product_search_form
from bakedpytato.widgets.manufacturer_select import ManufacturerSelect
from bakedpytato.widgets.scale_select import ScaleSelect

### Module Globals

logger = logging.getLogger(__name__)

colModel = [
	{'display':'Manufacturer', 'name':'manufacturer_name', 'width':200, 'align':'left'},
	{'display':'Identifier', 'name':'identifier', 'width':100, 'align':'left'},
	{'display':'Name', 'name':'name', 'width':200, 'align':'left'},
	{'display':'Stock', 'name':'stock', 'width':30, 'align':'left'},
	{'display':'Retail', 'name':'retail', 'width':30, 'align':'right'},
	{'display':'Cost', 'name':'cost', 'width':30, 'align':'right'},
	{'display':'Sale', 'name':'sale', 'width':30, 'align':'right'},
	{'display':'En', 'name':'archived', 'width':5, 'align':'right'},
	{'display':'Arch', 'name':'archived', 'width':5, 'align':'right'},
	{'display':'FIS', 'name':'archived', 'width':5, 'align':'right'},
]
 
buttons=[
	#{'name':'Add', 'bclass':'add', 'onpress': js_callback('add_record')},
	#{'name':'Delete', 'bclass':'delete', 'onpress': js_callback('delete_record')},
	{'separator':True}
]

product_grid = FlexiGrid(id='product_grid', fetchURL='/product/fetch', title='Products',
	colModel=colModel, useRp=True, rp='25',
	rpOptions=[10,25,50,100,200],
	sortname='identifier', sortorder='asc', usepager=True,
	showTableToggleButton=False,
	buttons=buttons,
	#width=1000,
	height=400,
)

class ProductController(BaseController):
	#Uncomment this line if your controller requires an authenticated user
	#allow_only = authorize.not_anonymous()

	@expose('bakedpytato.templates.product.index')
	def index(self):
		
		manufacturer_select = ManufacturerSelect('manufacturer_id')
		scale_select = ScaleSelect('scale_id')
		tmpl_context.product_grid = product_grid
		tmpl_context.manufacturer_select = manufacturer_select
		tmpl_context.scale_select = scale_select
		return dict()


	@validate(
		validators={
			"archived" : validators.StringBoolean(if_empty=None),
			"enabled" : validators.StringBoolean(if_empty=None),
			"identifier" : validators.String(if_empty=None),
			"in_stock" : validators.StringBoolean(if_empty=None),
			'manufacturer_id' : validators.UUID(if_empty=None),
			"name" : validators.String(if_empty=None),
			"not_archived" : validators.StringBoolean(if_empty=None),
			"not_enabled" : validators.StringBoolean(if_empty=None),
			"out_of_stock" : validators.StringBoolean(if_empty=None),
			"page" : validators.Int(if_empty=1), 
			"rp" : validators.Int(if_empty=50),
			'scale_id' : validators.UUID(if_empty=None),
			'sortname' : validators.String(if_empty='sort'),
			'sortorder' : validators.String(if_empty='asc'),
		}
	)
	@expose('json')
	def fetch(self, 
		archived = None, 
		not_archived = None, 
		enabled = None, 
		not_enabled = None, 
		identifier = None, 
		in_stock = None, 
		out_of_stock = None, 
		manufacturer_id = None, 
		name = None, 
		page = 1, 
		rp = 50, 
		scale_id = None, 
		sortname = 'sort', 
		sortorder = 'asc',
		**kw
	):
		try:
			offset = (page-1) * rp
			products = DBSession.query(ProductModel)

			e = []
			if enabled is not None:
				e.append(ProductModel.enabled == True)
			if not_enabled is not None:
				e.append(ProductModel.enabled == False)
			products = products.filter(or_(*e))
			
			e = []
			if archived is not None:
				e.append(ProductModel.archived == True)
			if not_archived is not None:
				e.append(ProductModel.archived == False)
			products = products.filter(or_(*e))

			e = []
			if in_stock is not None:
				e.append(ProductModel.stock > 0)
			if out_of_stock is not None:
				e.append(ProductModel.stock <= 0)
			products = products.filter(or_(*e))

			if identifier is not None:
				products = products.filter(ProductModel.identifier.ilike(identifier))
				
			if name is not None:
				products = products.filter(ProductModel.name.ilike(name))
			if manufacturer_id is not None:
				products = products.filter(ProductModel.manufacturer_id == manufacturer_id)
			if scale_id is not None:
				products = products.filter(ProductModel.scale_id == scale_id)

			total = products.count()

			if sortname in ['manufacturer', 'identifier']:
				sortname = 'sort'
			
			column = getattr(ProductModel, sortname)
			products = products.order_by(getattr(column,sortorder)())
			products = products.offset(offset).limit(rp)
			
			rows = [
				{
					'id'  : str(product.id),
					'cell': [
						product.manufacturer.name, 
						product.manufacturer.identifier + '-' + product.identifier, 
						product.name, 
						product.stock, 
						product.retail, 
						product.cost, 
						product.sale, 
						'En' if product.enabled else '',
						'Arc' if product.archived else '',
						'FIS' if product.force_in_stock else ''
					]
				} for product in products
			]
			return dict(page=page, total=total, rows=rows)
		except Exception:
			logger.exception("fetch failed")
