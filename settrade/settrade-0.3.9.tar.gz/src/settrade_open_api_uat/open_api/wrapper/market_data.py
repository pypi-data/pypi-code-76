from .lib import settrade_open_api as soa
from .util import send_python_error

class MarketData:
	def __init__(self, context, logger):
		self._context = context
		self._logger = logger
  
	def get_candlestick(
  	self,
		symbol,
   	interval,
		limit=500,
		start="",
		end="",
		is_adjusted=True,
  ):
		current_time = self._logger.get_current_time()

		try:
			interval_list = ["1m", "3m", "5m", "10m", "15m", "30m", "60m", "1d", "1w", "1M"]
  
			if interval not in interval_list:
				raise ValueError(interval + " is invalid. Please choose " + str(interval_list))
    
			result = soa.get_candlesticks(
				self._context,
				interval,
				symbol,
				limit,
				is_adjusted,
				start,
				end,
			)
   
			self._logger.write(current_time, "PYTHON_INFO", "get_candlesticks", "success")
   
			return result
		except Exception as err:
			self._logger.write(current_time, "PYTHON_EXCEPTION", "get_candlesticks", err)
   
			return send_python_error(err)