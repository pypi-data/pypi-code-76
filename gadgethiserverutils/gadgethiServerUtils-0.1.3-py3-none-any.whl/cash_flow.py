from encryption import *
from datetime import datetime
import time


def verify_finish_payment(intella_payment_data):
	"""
	This function verifies that the payment has been processed 
	Using dodaytest01 crypto class
	- Input:
		* intella_payment_data: Sent from Notification Payment Center
	- Output:
		* Integrity: Bool False/True
	"""
	iv =  b'8651731586517315'
	password = 'gdgth01'
	encryptor = GadgetEncryption(iv)

	try:
		Sign = intella_payment_data["Sign"]
		print ("Sign from intella = ",Sign)
		if Sign == "admin":
			return True
	except:
		pass
		
	if encryptor.verify(intella_payment_data):
		return True
	else:
		return False


def post_to_Intella(server_config, order_data, number_of_data):
	"""
	This function posts the order info to intella service and gets a url
	- Input:
		* order_data: dictionary of data
	- Return:
		* url: url of payment info
	"""

	# print ("order_data in post_to_Intella = ",order_data)

	StoreOrderNo = order_data['order_id']
	print ("StoreOrderNo = ",StoreOrderNo)
	Body = order_data['serial_number']
	print ("Body in post_to_Intella = ",Body)
	# Body += str(number_of_data) + '碗'
	TotalFee = str(order_data['total_price'])
	print ("TotalFee in post_to_Intella = ",TotalFee)
	"""
	Only for AWS
	"""
	if server_config["server_location"] == "AWS":
		shift_timezone = int(server_config["time_zone"])
	elif server_config["server_location"] == "local":	
		shift_timezone = 0
	cTime = int(datetime.now().timestamp()) + (shift_timezone*60*60)
	print(time.strftime("%Y%m%d%H%M%S", time.localtime(cTime)))
	time_str = time.strftime("%Y%m%d%H%M%S", time.localtime(cTime))
	iv =  b'8651731586517315'
	password = 'doday0618'
	# data_info = "{\"DeviceInfo\":\"skb0001\",\"StoreOrderNo\":\"PO-20200511-002\",\"Body\":\"Chicken Rice\",\"TotalFee\":\"1\"}"
	# data_info = {"DeviceInfo":"skb0001","StoreOrderNo":StoreOrderNo,"Body":Body,"TotalFee":TotalFee,"CallBackUrl":"https://gadget-hitech.com.tw/website_home.html","Delay":"3"}

	data_info = {"DeviceInfo":"skb0001","StoreOrderNo":StoreOrderNo,"Body":"訂單"+str(Body),"TotalFee":TotalFee,"CallBackUrl":"http://order.doday.com.tw/success_page.html","Delay":"3"}

	test_data ={
	  "Header": {
		"Method": "00000",
		"ServiceType":"OLPay",
		"MchId": "dodaytest01",
		"TradeKey": "73c70f3f4b2cf1dd69f729b89c986728c90fd42d84c902fa15abc01b2067de34",
		"CreateTime": time_str
	  },
		"Data": json.dumps(data_info)
	}	
	# print ("test_data = ",test_data['Data'])
	encryptor = GadgetEncryption(iv)
	# print(encryptor.generateRequestDict(test_data))
	payload = str(encryptor.generateRequestDict(test_data))
	payload.replace("\'","\"")
	print ("Intella encode payload = ",(payload))
	payload = ast.literal_eval(payload)
	# print ("New type = ",type(payload))
	intella_response = (encryptor.client_post(payload))
	intella_response = ast.literal_eval(intella_response)
	# print ("Intella response = ",(intella_response))
	intella_response = encryptor.decodeIntellaResponse(intella_response)
	intella_response = ast.literal_eval(intella_response)
	print ("Intella response = ",intella_response)
	return intella_response






def poll_multiple_orders(server_config,interval = 30000):
	"""
	This function uses the Intella multiple order polling.

	Request should be 

	{
	  "Header": {
		"Method": "00000",
		"ServiceType": "OrderQuery",
		"MchId": "myMchId",
		"TradeKey": "9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0",
		"CreateTime": "20180715105349"
	  },
	  "Data": "{\"StartDate\":\"20180715\",\"EndDate\":\"20180716\",\"OrderStatus\":\"1\"}"
	}
	
	Response may be 

	{
	  "Header": {
		"StatusCode": "0000",
		"StatusDesc": "執行成功",
		"Method": "00000",
		"ServiceType": "OrderQuery",
		"MchId": "myMchId"
	  },
	  "Data": {
		"DataValue": [
		  {
			"StoreOrderNo": "PO-20180715-004",
			"SysOrderNo": "104605",
			"TotalFee": 10,
			"FeeType": "TWD",
			"Status": "Trade success",
			"Description": "-7082",
			"Method": "11500"
		  },
		  {
			"StoreOrderNo": "PO-20180715-005",
			"SysOrderNo": "104644",
			"TotalFee": 10,
			"FeeType": "TWD",
			"Status": "Trade success",
			"RefundStatus": "Refund success",
			"Description": "Chicken Rice-0247",
			"Method": "31800"
		  }
		]
	  }
	}

	"""

	"""
	Only for AWS
	"""
	if server_config["server_location"] == "AWS":
		shift_timezone = server_config["time_zone"]
	elif server_config["server_location"] == "local":	
		shift_timezone = 0
	cTime = int(datetime.now().timestamp()) + (shift_timezone*60*60)
	start_time = int(cTime - interval)
	print("Current time = ",time.strftime("%Y%m%d%H%M%S", time.localtime(cTime)))
	current_time_str = time.strftime("%Y%m%d%H%M%S", time.localtime(cTime))
	start_time_str = time.strftime("%Y%m%d%H%M%S", time.localtime(start_time))
	print ("Start time = ",start_time_str)
	iv =  b'8651731586517315'
	password = 'gdgth01'
	# data_info = "{\"DeviceInfo\":\"skb0001\",\"StoreOrderNo\":\"PO-20200511-002\",\"Body\":\"Chicken Rice\",\"TotalFee\":\"1\"}"
	data_info = {"StartDate":start_time_str,"EndDate":current_time_str,"OrderStatus":"1"}
	test_data ={
	  "Header": {
		"Method": "00000",
		"ServiceType":"OrderQuery",
		"MchId": "dodaytest01",
		"TradeKey": "73c70f3f4b2cf1dd69f729b89c986728c90fd42d84c902fa15abc01b2067de34",
		"CreateTime": current_time_str
	  },
		"Data": json.dumps(data_info)
	}	
	# print ("test_data = ",test_data['Data'])
	encryptor = GadgetEncryption(iv)
	# print(encryptor.generateRequestDict(test_data))
	payload = str(encryptor.generateRequestDict(test_data))
	payload.replace("\'","\"")
	# print ("Intella encode type = ",type(payload))
	payload = ast.literal_eval(payload)
	# print ("New type = ",type(payload))
	intella_response = (encryptor.client_post(payload))
	intella_response = ast.literal_eval(intella_response)
	# print ("Intella response = ",(intella_response))
	intella_response = encryptor.decodeIntellaResponse(intella_response)
	intella_response = ast.literal_eval(intella_response)
	return intella_response




# if __name__ == '__main__':
# 	while True:
# 		poll_multiple_orders()
# 		time.sleep(2)

























