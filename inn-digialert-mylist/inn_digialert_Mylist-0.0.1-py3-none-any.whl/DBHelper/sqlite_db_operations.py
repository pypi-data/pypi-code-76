import sqlite3
from sqlite3 import Error
import DBHelper.dbddl as ddl
import json


class DBMyList:
	conn = None
	active_cursor = None
	set_sequence = """delete from sqlite_sequence where name='TASKS' """

	def __init__(self, database_name):
		self.database_name = database_name

	def close(self):
		self.conn.close()

	def create_connection(self):
		conn = None
		try:
			conn = sqlite3.connect(self.database_name, check_same_thread=False)
			conn.isolation_level = None
		except Error as conn_error:
			print("Exception: create_connection:", conn_error)

		except Exception as e_all:
			print("Exception: create_connection:", e_all)

		finally:
			self.conn = conn

	def create_table(self, ddl_to_create_table):
		if self.conn is None:
			return False
		else:
			try:
				db_cursor = self.conn.cursor()
				operation_status = db_cursor.execute(ddl_to_create_table)
				return True, operation_status
			except Exception as create_error:
				print("Exception:create_table",create_error)
				return False, "Exception"

	def create_task(self, insert_sql, task):
		# create own cursor for each transaction
		if self.active_cursor is None:
			self.active_cursor = self.conn.cursor()
		trx_cursor = self.conn.cursor()
		'''
		self.active_cursor.execute(insert_sql, task)
		self.conn.commit()
		self.active_cursor.execute(ddl.max_id)
		return self.active_cursor.fetchone()[0]
		'''
		trx_cursor.execute(insert_sql, task)
		self.conn.commit()
		trx_cursor.execute(ddl.max_id)
		return trx_cursor.fetchone()[0]


	def update_task_title(self, update_sql, task):

		trx_cursor = self.conn.cursor()
		trx_cursor.execute(update_sql, task)
		update_status = None
		if trx_cursor.rowcount >= 0:
			print("update successful", task)
			update_status = "Update Successful"
		else:
			print("update failed", task)
			update_status = "Update Failed"
		self.conn.commit()
		return update_status

	def update_is_done(self, update_sql, task):

		trx_cursor = self.conn.cursor()
		trx_cursor.execute(update_sql, task)
		self.conn.commit()

	def delete_task(self, delete_sql, task):

		#  trx_cursor = self.conn.cursor()
		trx_cursor = sqlite3.connect(self.database_name, check_same_thread=False).cursor()
		trx_cursor.execute("begin")
		trx_cursor.execute(delete_sql, task)
		if trx_cursor.rowcount > 0:  # commit only when delete was successful
			# self.conn.commit()
			trx_cursor.execute("commit")
		return trx_cursor.rowcount

	def select_by_id(self, sql, task_id):
		trx_cursor = self.conn.cursor()
		trx_cursor.execute(sql, task_id)
		rows = trx_cursor.fetchall()
		return rows

	def select_by_is_done(self, sql, is_done):
		trx_cursor = self.conn.cursor()

		trx_cursor.execute(sql, is_done)
		rows = trx_cursor.fetchall()
		return rows

	def select_all(self, sql):
		trx_cursor = self.conn.cursor()
		trx_cursor.execute(sql)
		rows = trx_cursor.fetchall()
		return rows

	def select_is_done_status(self, sql, status):
		trx_cursor = self.conn.cursor()
		trx_cursor.execute(sql, status)
		rows = trx_cursor.fetchall()
		print("+++++Status+++++++")
		for each in rows:
			print(each)

	def delete_all_tasks(self, delete_sql):
		trx_cursor = self.conn.cursor()
		trx_cursor.execute(delete_sql)
		self.conn.commit()
		deleted_rows = trx_cursor.rowcount
		trx_cursor.execute(self.set_sequence)
		return deleted_rows

