import aiosqlite
import asyncio

class EconomyCord:
    def __init__(self, database_dir="", starting_balance=0, auto_check_users=True):
        self.database=None
        self.database_dir=database_dir
        self.starting_balance=starting_balance
        self.auto_check=auto_check_users
        self.loop=asyncio.new_event_loop()
        self.loop.run_until_complete(self.connect_to_db())

    async def connect_to_db(self):
        self.database=await aiosqlite.connect(f'{self.database_dir}data.db')
        c=await self.database.cursor()
        try:
            try:
                await c.execute("ALTER TABLE users ADD item1 TEXT DEFAULT ''")
                await c.execute("ALTER TABLE users ADD item2 TEXT DEFAULT ''")
                await c.execute("ALTER TABLE users ADD item3 TEXT DEFAULT ''")
                await c.execute("ALTER TABLE users ADD item4 TEXT DEFAULT ''")
                await c.execute("ALTER TABLE users ADD item5 TEXT DEFAULT ''")
            except:
                await c.execute("CREATE TABLE IF NOT EXISTS users (userid INTEGER, balance INTEGER, bank INTEGER DEFAULT 0, UNIQUE(userid))")
            await self.database.commit()
        except Exception as e:
            return print(e)

    async def insert_user(self, userid):
        c=await self.database.cursor()
        try:
            await c.execute("INSERT INTO users (userid, balance) VALUES (?, ?) ON CONFLICT DO NOTHING", (userid, self.starting_balance))
            await self.database.commit()
        except Exception as e:
            print(e)

    async def check_user(self, userid):
        await self.insert_user(userid)

    async def get_balance(self, userid):
        c=await self.database.cursor()
        if self.auto_check:
            await self.check_user(userid)
        await c.execute("SELECT balance FROM users WHERE userid=?", (userid,))
        user_results=await c.fetchone()
        return user_results[0]
    
    async def get_bank(self, userid):
        c=await self.database.cursor()
        if self.auto_check:
            await self.check_user(userid)
        await c.execute("SELECT bank FROM users WHERE userid=?", (userid,))
        user_results=await c.fetchone()
        return user_results[0]

    async def add_balance(self, userid, amount:int):
        c=await self.database.cursor()
        if self.auto_check:
            await self.check_user(userid)
        before_balance=await self.get_balance(userid)
        new_balance=before_balance+amount
        await c.execute("UPDATE users SET balance=? WHERE userid=?", (new_balance, userid))

    async def add_bank(self, userid, amount:int):
        c=await self.database.cursor()
        if self.auto_check:
            await self.check_user(userid)
        before_bank=await self.get_bank(userid)
        new_bank=before_bank+amount
        await c.execute("UPDATE users SET bank=? WHERE userid=?", (new_bank, userid))

    async def remove_balance(self, userid, amount:int):
        c=await self.database.cursor()
        if self.auto_check:
            await self.check_user(userid)
        before_balance=await self.get_balance(userid)
        new_balance=before_balance-amount
        await c.execute("UPDATE users SET balance=? WHERE userid=?", (new_balance, userid))

    async def remove_bank(self, userid, amount:int):
        c=await self.database.cursor()
        if self.auto_check:
            await self.check_user(userid)
        before_bank=await self.get_bank(userid)
        new_bank=before_bank-amount
        await c.execute("UPDATE users SET bank=? WHERE userid=?", (new_bank, userid))

    async def get_top_by_balance(self, limit=10):
        c=await self.database.cursor()
        await c.execute(f"SELECT userid, balance FROM users ORDER BY balance desc")
        user_results=await c.fetchall()
        user_results=user_results[:(limit)]
        user_results=[{'userid': result[0], 'balance': result[1]} for result in user_results]
        user_results=sorted(user_results, key=lambda d: d['balance'])
        return user_results

    async def get_top_by_bank(self, limit=10):
        c=await self.database.cursor()
        await c.execute(f"SELECT userid, bank FROM users ORDER BY bank desc")
        user_results=await c.fetchall()
        user_results=user_results[:(limit)]
        user_results=[{'userid': result[0], 'bank': result[1]} for result in user_results]
        user_results=sorted(user_results, key=lambda d: d['bank'])
        return user_results

    async def get_top_by_both(self, limit=10):
        c=await self.database.cursor()
        await c.execute(f"SELECT userid, balance, bank FROM users")
        user_results=await c.fetchall()
        user_results=user_results[:(limit)]
        user_results=[{'userid': result[0], 'both': (result[1]+result[2])} for result in user_results]
        user_results=sorted(user_results, key=lambda d: d['both'])
        return user_results
    
    async def transfer_balance(self, fromid, toid, amount):
        c=await self.database.cursor()
        if self.auto_check:
            await self.check_user(fromid)
            await self.check_user(toid)
        fromid_before_bank=await self.get_bank(fromid)
        fromid_new_bank=fromid_before_bank-amount
        await c.execute("UPDATE users SET balance=? WHERE userid=?", (fromid_new_bank, fromid))
        toid_before_bank=await self.get_bank(toid)
        toid_new_bank=toid_before_bank+amount
        await c.execute("UPDATE users SET balance=? WHERE userid=?", (toid_new_bank, toid))
        await self.database.commit()