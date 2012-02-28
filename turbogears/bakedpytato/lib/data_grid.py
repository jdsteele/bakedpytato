from sqlalchemy import asc, desc
from tw.forms.datagrid import Column
import genshi
from tg import request, url

from tw.forms import DataGrid

class SortableDataGrid(DataGrid):
	pass

	def find_col(self, name):
		for field in self.fields:
			if isinstance(field, Column):
				if field.name == name:
					return field

class SortableColumn(Column):
	
	def __init__(self, title, name, sa_col=None):
		super(SortableColumn, self).__init__(name)
		self._title_ = title
		self._sa_col_ = sa_col

	def get_sa_col(self):
		if self._sa_col_ is not None:
			return self._sa_col_
		return self.name

	def set_title(self, title):
		self._title_ = title

	def get_title(self):
		sort_col = request.GET.get('sort_col')
		
		if sort_col and sort_col == self.name:
			sort_dir = request.GET.get('sort_dir')
			if sort_dir == 'desc':
				sort_dir = 'asc'
				arrow = '&#x21D1;'
			else:
				sort_dir = 'desc'
				arrow = '&#x21D3;'
		else:
			sort_dir = 'asc'
			arrow = ''
		sort_col = self.name

		new_params = dict(request.GET)
		new_params['sort_col'] = sort_col
		new_params['sort_dir'] = sort_dir

		new_url = url(request.path_url, params=new_params)
		return genshi.Markup('<a href="%(page_url)s">%(title)s %(dir)s</a>' % dict(page_url=new_url, title=self._title_, dir=arrow))

	title = property(get_title, set_title)
	sa_col = property(get_sa_col)
