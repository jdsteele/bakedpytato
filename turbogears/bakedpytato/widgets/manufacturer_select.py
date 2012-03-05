from bakedpytato.model import DBSession, ManufacturerModel
from tw.forms import SingleSelectField
import time

timestamp = time.time()
options = []

class ManufacturerSelect(SingleSelectField):
   def update_params(self, d):
		rows = DBSession.query(ManufacturerModel)
		rows = rows.filter(ManufacturerModel.display == True)
		rows = rows.order_by(ManufacturerModel.sort)
		options = [(None, '-')]
		for row in rows:
			options.append(
				(
					row.id, 
					"{n:.32} - ({i})".format(
						n=row.name, 
						i=row.identifier
					)
				)
			)
		d['options'] = options
		SingleSelectField.update_params(self, d)
		return d
