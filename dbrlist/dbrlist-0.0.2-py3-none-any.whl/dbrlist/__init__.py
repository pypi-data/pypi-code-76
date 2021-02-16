import aiohttp

class Client:
    def __init__(self, key):
        self.key = key
        self.session = aiohttp.ClientSession()
        self.base_url = 'https://discordbotlist.com/api/v1'
    
    async def get(self, route, *, params={}, headers={}):
        async with self.session.get(self.base_url + route, params=params, headers=headers) as resp:
            return await resp.json()
    
    async def post(self, route, *, params={}, headers={}):
        async with self.session.post(self.base_url + route, params=params, headers=headers) as resp:
            return resp.status
    
    async def metrics(self, id):
        return (await self.get(f'/bots/{id}/'))['metrics']
    
    async def stats(self, id):
        return (await self.get(f'/bots/{id}/'))['stats']
    
    async def post_stats(self, id, guilds, *, voice_connections=None, users=None, shard_id=None):
        return await self.post(f'/bots/{id}/stats', params={'guilds': guilds, 'voice_connections': voice_connections, 'users': users, 'shard_id': shard_id}, headers={'Authorization': self.key})
