import Database as DB
db = DB.Database("admin", "db-admin", "jarvis")
db.table("test").delete()
db.table("test").insert({"hello": "world"})
db.table("test").filter({"hello": "world"}).update({"hello2":"world2"})
