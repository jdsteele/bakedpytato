from bakedpytato.model import DBSession, ScaleModel
from tw.forms import SingleSelectField
import time

timestamp = time.time()
options = []

class ScaleSelect(SingleSelectField):
   def update_params(self, d):
		rows = DBSession.query(ScaleModel)
		#rows = rows.filter(ScaleModel.display == True)
		rows = rows.order_by(ScaleModel.name)
		options = [(None, '-')]
		for row in rows:
			options.append(
				(
					row.id, 
					row.name, 
				)
			)
		d['options'] = options
		SingleSelectField.update_params(self, d)
		return d
