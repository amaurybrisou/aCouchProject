from datetime import datetime
from dateutil.relativedelta import relativedelta

class Dates:
	@staticmethod
	def expirationDate():
		return datetime.today()+ relativedelta(months=1)

	@staticmethod
	def UTCNow():
		return datetime.utcnow()