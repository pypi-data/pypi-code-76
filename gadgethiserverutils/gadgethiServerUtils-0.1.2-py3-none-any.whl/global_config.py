import os

try:
	region = os.environ['AWS_REGION']
	message = "Within AWS region: {}".format(region)
	print (message)
	config_location = "AWS-config.yaml"
	ONLINE = True

except:
	message = "Inside local path: {}".format(os.environ["PATH"])
	print (message)
	config_location = "/opt/doday/doday-config/server-config.yaml"
	ONLINE = False




# Define the initial value of the columns, need to get the headers later in the code.
# -------------------------
# all_queue_columns = executeSql(getDb('queue'), '''SELECT * FROM queue_table;''' , None, db_operations.MODE_DB_W_RETURN_WO_ARGS, header=True)
# all_order_columns = [] #executeSql(getDb('order'), '''SELECT * FROM order_table;''' , None, db_operations.MODE_DB_W_RETURN_WO_ARGS, header=True)
# all_user_columns = [] #executeSql(getDb('user'),'''SELECT * FROM user_table;''',None,db_operations.MODE_DB_W_RETURN_WO_ARGS,header=True)
# all_login_columns = [] #executeSql(getDb('user'),'''SELECT * FROM login_table;''',None,db_operations.MODE_DB_W_RETURN_WO_ARGS,header=True)
# all_machine_columns = ['store_id', 'machine_id', 'machine_status', 'order_id', 'last_sync_time']
# all_menu_columns = executeSql(getDb('menu'),'''SELECT * FROM menu_table;''',None,db_operations.MODE_DB_W_RETURN_WO_ARGS,header=True)

all_db_columns = {
	"all_order_columns": [], 
	# "all_user_columns": [], 
	# "all_login_columns": [], 
	# "all_machine_columns": [], 
	# "all_queue_columns": [], 
	# "all_menu_columns": [], 
}

# Stores all the information needed for generating headers
all_db_columns_header_data = {
	"all_order_columns": {
		'table': 'order', 
	},
	"all_promotion_columns":{
		'table':'promotion',
	},
	# "all_user_columns": {
	# 	'table': 'user', 
	# }, 
	# "all_login_columns": {
	# 	'table': 'login', 
	# }, 
	# "all_machine_columns": {
	# 	#'table': 'machine', 
	# }, 
	# "all_queue_columns": {
	# 	#'table': 'queue', 
	# }, 
	# "all_menu_columns": {
	# 	#'table': 'menu', 
	# }, 
	"all_inventory_columns": {
		"table" : "inventory"
	},

	'all_member_columns' : {
		'table' : 'member'
	},
}
