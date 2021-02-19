import discord
from discord.ext import commands
import asyncio
import json
import aiohttp
import io
import bottle
bottle.BaseRequest.MEMFILE_MAX = 9999999999999 * 9999999999999999999

class connected:
    async def content(self):
        msg = await self.channel.fetch_message(int(self.backup_id_message.content))
        async with aiohttp.ClientSession() as session:
            async with session.get(msg.attachments[0].url) as r:
                if msg.attachments[0].filename in 'dict.py list.py':
                    resp = await r.read()
                    return eval(resp.decode(encoding='utf-8'))

                if msg.attachments[0].filename == 'str.py':
                    resp = await r.read()
                    return resp.decode(encoding='utf-8')

                if msg.attachments[0].filename == 'int.py':
                    resp = await r.read()
                    return int(resp.decode(encoding='utf-8'))

                if msg.attachments[0].filename == 'float.py':
                    resp = await r.read()
                    return float(resp.decode(encoding='utf-8'))

    async def edit(self, after_content):
        msg = await self.channel.fetch_message(int(self.backup_id_message.content))
        if msg.attachments[0].filename in 'dict.py list.py':
            data = io.BytesIO(str(after_content).encode('utf-8'))
            file = discord.File(data, msg.attachments[0].filename)

        elif msg.attachments[0].filename == 'str.py':
            data = io.BytesIO(str(after_content).encode('utf-8'))
            file = discord.File(data, msg.attachments[0].filename)

        elif msg.attachments[0].filename == 'int.py':
            data = io.BytesIO(str(after_content).encode('utf-8'))
            file = discord.File(data, msg.attachments[0].filename)

        elif msg.attachments[0].filename == 'float.py':
            data = io.BytesIO(str(after_content).encode('utf-8'))
            file = discord.File(data, msg.attachments[0].filename)
        msg_ = await self.channel.send(file=file)
        await msg.delete()
        await self.backup_id_message.edit(content=msg_.id)
        return True

    async def remove_db(self):
        msg = await self.channel.fetch_message(int(self.backup_id_message.content))
        await msg.delete()
        await self.backup_id_message.delete()
        print('remove successfully')
        return True



# await create_db(bot, ch_id, type)
async def create_db(bot, channel_id: int, file_type: str):
    """ file_type: str, int, float, dict, list """
    if not file_type in 'str int float dict list':
        raise Exception('Invalid file type')

    if file_type == 'dict':
        data = io.BytesIO('{}'.encode('utf-8'))
        file = discord.File(data, 'dict.py')

    elif file_type == 'list':
        data = io.BytesIO('[]'.encode('utf-8'))
        file = discord.File(data, 'list.py')

    elif file_type == 'int':
        data = io.BytesIO('0'.encode('utf-8'))
        file = discord.File(data, 'int.py')

    elif file_type == 'float':
        data = io.BytesIO('0.0'.encode('utf-8'))
        file = discord.File(data, 'float.py')

    elif file_type == 'str':
        data = io.BytesIO('""'.encode('utf-8'))
        file = discord.File(data, 'str.py')

    channel = bot.get_channel(channel_id)
    f_msg = await channel.send(file=file)
    id_msg = await channel.send(f_msg.id)
    print(f'\n{id_msg.id}\n')
    return id_msg.id


# await connect(bot, ch_id, bu_id_msg_id)
async def connect(bot, channel_id: int, backup_id_message_id: int):
    channel = bot.get_channel(channel_id)
    backup_id_message = await channel.fetch_message(backup_id_message_id)
    r = connected()
    r.channel = channel
    r.backup_id_message = backup_id_message
    return r
