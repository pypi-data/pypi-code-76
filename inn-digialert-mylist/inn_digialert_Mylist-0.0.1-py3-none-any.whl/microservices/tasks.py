from flask import Flask
from flask import jsonify, make_response, request
import secrets

import DBHelper.sqlite_db_operations as my_db
import DBHelper.dbddl as ddl

myList_app = Flask(__name__)
api_key_length = 24
api_key = None

#db_my_list = my_db.DBMyList("MYList.db")
#db_my_list.create_connection()
db_my_list = None

@myList_app.route('/')
def return_authentication_code():
	global api_key
	global db_my_list
	db_my_list = my_db.DBMyList("MYList.db")
	db_my_list.create_connection()

	# debug only
	if api_key:
		pass
	else:
		api_key = secrets.token_urlsafe(api_key_length)

	# api_key = secrets.token_urlsafe(api_key_length)
	response_dict = {'api_key': api_key}
	return response_dict, 200


@myList_app.route('/add_task', methods=['POST'])  # add a new task
def add_task():
	global api_key
	global db_my_list
	'''
	payload:
	{
	task_title:"Buy Bread"
	is_done: 0
	}
	response:
	id(new task),response code
	'''
	payload_api_key = request.headers.get('API-Key')
	response_dict = {}
	status_code = None
	print("Add task api key:",payload_api_key)
	if payload_api_key == api_key:
		response_dict['Success'] = "Request Authenticated"
		status_code = 200
		print("request:",request.data)
		request_json = request.get_json()
		print("Request json:", request_json)
		task_title = request_json.get("task_title")
		is_done = request_json.get("is_done")

		if task_title and is_done:
			max_id = db_my_list.create_task(ddl.insert_task, (task_title, is_done))
			response_dict["id"] = max_id
		elif task_title:
			max_id = db_my_list.create_task(ddl.insert_task, (task_title, 0))
			response_dict["id"] = max_id
		else:
			response_dict["Error"] = "Task name missing"
	else:
		response_dict['Failure'] = "Authorization Failed"
		status_code = 401
	return response_dict, status_code


@myList_app.route('/get_task/<int:taskid>', methods=['GET'])
def get_task_by_id(taskid):
	global api_key
	global db_my_list
	payload_api_key = request.headers.get('API-Key')
	response_dict = {}
	status_code = None
	if payload_api_key == api_key:
		response_dict['Success'] = "Request Authenticated"
		status_code = 200
		rowset = db_my_list.select_by_id(ddl.select_by_task_id, (taskid,))
		print("row set:", rowset)
		response_dict['task'] = rowset
	else:
		response_dict['Failure'] = "Authorization Failed"
		status_code = 401
	return response_dict, status_code


@myList_app.route('/get_task/status/<int:is_done>', methods=['GET'])
def get_tasks_by_status(is_done):
	global api_key
	global db_my_list
	payload_api_key = request.headers.get('API-Key')
	response_dict = {}
	status_code = None
	if payload_api_key == api_key:
		response_dict['Success'] = "Request Authenticated"
		status_code = 200
		rowset = db_my_list.select_by_id(ddl.select_by_is_done, (is_done,))

		response_dict['task'] = rowset
	else:
		response_dict['Failure'] = "Authorization Failed"
		status_code = 401
	return response_dict, status_code


@myList_app.route('/get_all_tasks', methods=['GET'])
def get_all_tasks():
	global api_key
	global db_my_list
	payload_api_key = request.headers.get('API-Key')
	response_dict = {}
	status_code = None
	if payload_api_key == api_key:
		response_dict['Success'] = "Request Authenticated"
		status_code = 200
		rowset = db_my_list.select_all(ddl.select_all)
		response_dict['task'] = rowset
	else:
		response_dict['Failure'] = "Authorization Failed"
		status_code = 401
	return response_dict, status_code


@myList_app.route('/tasks/put', methods=['PUT'])
def update_task_status():
	global api_key
	global db_my_list
	payload_api_key = request.headers.get('API-Key')
	response_dict = {}
	status_code = None
	if payload_api_key == api_key:
		response_dict['Success'] = "Request Authenticated"
		status_code = 200
		request_json = request.get_json()
		print(request_json)
		try:
			task_id = request_json.get("id")
			is_done = request_json.get("is_done")
			update_status = db_my_list.update_is_done(ddl.update_is_done,(is_done,task_id))
			response_dict["Update_Status"] = update_status
		except Exception as e:
			response_dict["Error"] = "Request data missing; Error" + str(e)
	else:
		response_dict['Failure'] = "Authorization Failed"
		status_code = 401
	return response_dict, status_code


@myList_app.route('/tasks/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
	global api_key
	global db_my_list
	payload_api_key = request.headers.get('API-Key')
	response_dict = {}
	status_code = None
	if payload_api_key == api_key:
		response_dict['Success'] = "Request Authenticated"
		status_code = 200
		rows_deleted = db_my_list.delete_task(ddl.delete_task, (task_id,))
		# print("rowset:", rowset)
		if rows_deleted > 0:
			response_dict['rows_deleted'] = rows_deleted
			response_dict['task_id'] = task_id
		else:
			response_dict['Error'] = "No item to delete"
			response_dict['task_id'] = task_id

	else:
		response_dict['Failure'] = "Authorization Failed"
		status_code = 401
	return response_dict, status_code


@myList_app.route('/tasks/delete_all', methods=['POST', 'DELETE'])
def delete_all_the_tasks():
	global api_key
	global db_my_list
	payload_api_key = request.headers.get('API-Key')
	response_dict = {}
	status_code = None
	if payload_api_key == api_key:
		response_dict['Success'] = "Request Authenticated"
		status_code = 200
		rows_deleted = db_my_list.delete_all_tasks(ddl.delete_all_tasks)
		response_dict['rows_deleted'] = rows_deleted
	else:
		response_dict['Failure'] = "Authorization Failed"
		status_code = 401
	return response_dict, status_code


def start_the_server():
	global api_key
	api_key = secrets.token_urlsafe(api_key_length)
	'''
	if need to run flask on same wifi:
	1. run the flask with host 
	#myList_app.run(host="0.0.0.0")  
	2. get the ip on mac can find with command ipconfig getifaddr en1
	for mobile or any device on same wifi, access 
	xxx.xxx.x.xxxx:5000 and flask will return routed: @myList_app.route('/')
	
	'''
	myList_app.run(host="0.0.0.0", threaded=True)
	#myList_app.run()




