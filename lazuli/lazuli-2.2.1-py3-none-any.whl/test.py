import mysql.connector as con

database_config = {
	'host': 'localhost',
	'user': 'root',
	'password': '',
	'schema': 'kms_316',
	'port': 3306
}


def get_db(config, query):
	"""Generic static method for fetching data from DB using the provided DB config and query

	This method assumes that only one character is found - it always defaults to the first result.
	An effort has been made to convert this to a decorator so that it may also be applied to
	Character::set_stat_by_column() & Character::get_user_id(), which ultimately ended in failure.

	Args:
		config, dictionary, representing database config attributes
		query, String, representing SQL query
	Returns:
		String representing the result of the provided SQL query, using the provided DB connection attributes
	"""
	try:
		database = con.connect(
			host=config["host"],
			user=config["user"],
			password=config["password"],
			database=config["schema"],
			port=config["port"]
		)
		cursor = database.cursor(dictionary=True)
		cursor.execute(query)
		data = cursor.fetchall()[0]
		database.disconnect()

		return data

	except Exception as e:
		print("CRITICAL: Error encountered whilst attempting to connect to the database! \n", e)


# print("Now fetching Character data from AzureMS DB: \n")
#
# character = get_db(
# 	database_config,
# 	f"SELECT * FROM characters WHERE name = 'Soul'"
# )
# character.pop('hope')
#
# print(character, "\n")
# print("------------------------------------------------")
# print("Now fetching Inventory data from AzureMS DB: \n")
#
# inventory = get_db(
# 	database_config,
# 	f"SELECT * FROM inventoryitems WHERE characterid = 3"
# )
#
#
# print(inventory)

# print("------------------------------------------------")
# print("Now fetching Inventory data from AzureMS DB: \n")
#
# database = con.connect(
# 			host=database_config["host"],
# 			user=database_config["user"],
# 			password=database_config["password"],
# 			database=database_config["schema"],
# 			port=database_config["port"]
# 		)
# cursor = database.cursor(dictionary=True)
# cursor.execute(f"SELECT * FROM inventoryitems WHERE characterid = 3")
# data = cursor.fetchall()
# database.disconnect()
# print(data)
