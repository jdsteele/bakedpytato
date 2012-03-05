"""Movie Form"""

from tw.api import WidgetsList
from tw.forms import TableForm, CalendarDatePicker, SingleSelectField, TextField, TextArea


class ProductSearchForm(TableForm):

	class fields(WidgetsList):
		identifier = TextField()

product_search_form = ProductSearchForm("product_search_form", action='page')
