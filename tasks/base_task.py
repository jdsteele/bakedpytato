from session import Session

class BaseTask(object):
	logref = None
	
	def __init__(self):
		"""Init"""
		self.session = Session(autocommit=True)
