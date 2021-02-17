import datetime
import time
import logging

def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def check_operation_hours(**kwargs):
	"""
	Given opening_time, closing_time. 
	return True if it's is within operation hours. 
	return False if not.
	"""
	opening_time, closing_time = kwargs["opening_time"], kwargs["closing_time"]

	opening_hour, opening_minute = int(opening_time[:2]), int(opening_time[3:])
	closing_hour, closing_minute = int(closing_time[:2]), int(closing_time[3:])
	logging.info("[VerifyOperationHour] opening_hour, closing_hour = "+ str(opening_hour) + str(closing_hour))

	start_time = datetime.time(opening_hour,opening_minute)
	end_time = datetime.time(closing_hour,closing_minute)
	current_time = datetime.datetime.now().time()

	return is_time_between(start_time, end_time, current_time)