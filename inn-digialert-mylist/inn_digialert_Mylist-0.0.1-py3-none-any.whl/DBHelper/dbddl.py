ddl_create_task_table = """CREATE TABLE IF NOT EXISTS TASKS (
						id integer  PRIMARY KEY AUTOINCREMENT, task_title text, is_done integer) """

insert_task = """insert into TASKS(task_title,is_done) values(?,?)"""

update_task_title = "UPDATE TASKS set task_title = ? where id = ? "

update_is_done = "UPDATE TASKS set is_done= ? where id = ? "

max_id = "SELECT max(id) from TASKS"

delete_task = "DELETE from TASKS where id=?"

delete_all_tasks = "DELETE  from TASKS"

select_all = "select * from TASKS"

select_all_is_done_status = "Select * from TASKS where is_done = ? "

select_by_task_id = "Select * from TASKS where id =?"

select_by_is_done = "Select * from TASKS where is_done =?"

