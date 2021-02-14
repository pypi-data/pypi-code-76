class dbot():
	def __init__(self, info):
		import os
		try:
			import discord
			from discord.ext import commands
		except:
			print("Нет модуля discord, начинаем установку!")
			os.system("pip install discord")
		try:
			import asyncio
		except:
			print("Нет модуля asyncio, начинаем установку!")
			os.system("pip install asyncio")
		try:
			import PIL
		except:
			print("Нет модуля pillow, начинаем установку!")
			os.system("pip install pillow")
		try:
			import requests
		except:
			print("Нет модуля requests, начинаем установку!")
			os.system("pip install requests")
		try:
			import io
		except:
			print("Нет модуля io, начинаем установку!")
			os.system("pip install io")
		import discord
		from discord.ext import commands
		self._prefix=info["prefix"]
		self._token=info["token"]
		try:
			self._type=info["type"]
		except:
			self._type="ping"
		try:
			self._self=info["self"]=="true"
		except:
			self._self=False
		try:
			self._path=info["path"][:len(info["path"])-len(os.path.basename(info["path"]))]+"vars.db"
		except Exception as e:
			self._path="vars.db"
		self._codes={}
		self._count=0
		self._codes["commands"]={}
		self._client=commands.Bot(command_prefix=self._prefix, intents=discord.Intents.all())
		self._client.remove_command(help)

	def command(self, info):
		self._count+=1
		self._codes["commands"][self._count]={}
		code=[]
		try:
			code=list(info["code"])
		except:
			for n in info:
				if not n in ["name","prefix"]:
					code.append(info[n])
		self._codes["commands"][self._count]["name"]=info["name"]
		self._codes["commands"][self._count]["code"]=code
		try:
			self._codes["commands"][self._count]["prefix"]=info["prefix"]
		except:
			self._codes["commands"][self._count]["prefix"]=self._prefix

	def start(self):
		_start(self._client, self)

def _start(client, info):
	
	@client.event
	async def on_ready():
		print("Бот онлайн!")
	
	@client.event
	async def on_message(message):
		if not message.author.bot:
			if info._type=="ping":
				def remember(text):
					global command
					command = text
					return True
				if any(message.content.startswith(info._codes["commands"][cmd]["prefix"]+info._codes["commands"][cmd]["name"]) and remember(cmd) for cmd in info._codes["commands"]):
					await use([message, command, "commands"],info)
			elif info._type=="all":
				for cmd in info._codes["commands"]:
					if message.content.startswith(info._codes["commands"][cmd]["prefix"]+info._codes["commands"][cmd]["name"]):
						await use([message, cmd, "commands"],info)
	if info._self:
		client.run(info._token, bot=False)
	else:
		client.run(info._token)

async def use(need, info):
	import discord
	import io
	from PIL import Image
	import requests
	import datetime
	binstr = ""
	content = need[0].content[len(info._codes[need[2]][need[1]]["prefix"]+info._codes[need[2]][need[1]]["name"]):].lstrip(" ")
	emb = [False, discord.Embed()]
	functions = {"$eval":"noarg","$title[":"arg","$description[":"arg","$color[":"arg","$addField[":"arg","$thumbnail[":"arg","$image[":"arg","$footer[":"arg","$author[":"arg","$authorIcon[":"arg","$footerIcon[":"arg","$deletecommand":"noarg","$addReactions[":"arg","$addCmdReactions[":"arg","$addTimestamp":"noarg","$authorURL[":"arg","$suppressErrors[":"arg","$embedSuppressErrors[":"arg","$addEmoji[":"arg"}
	lines = info._codes[need[2]][need[1]]["code"]
	reactions = []
	linec=0
	error=[True,""]
	if "$eval" in lines:
		lines=lines[:lines.index("$eval")]
		lines=lines + content.split("\n")
	for line in lines:
		linec+=1
		reline = line
		def remember(text):
			global function
			function = text
			return True
		if any(line.startswith(func) and remember(func) for func in functions):
			if functions[function]=="arg":
				reline = reline.replace("$authorID",str(need[0].author.id))
				reline = reline.replace("$message",content)
				if line.endswith("]"):
					line = reline
					line=line[:-1]
				else:
					if binstr == "":
						binstr += reline
					else:
						binstr += "\n"+reline
			try:
				if line.startswith("$title["):
					emb[1].title=line[len("$title["):]
					emb[0]=True
				elif line.startswith("$description["):
					emb[1].description=line[len("$description["):]
					emb[0]=True
				elif line.startswith("$color["):
					rgb=list(int(line[len("$color["):][i:i+2], 16) for i in (0, 2, 4))
					emb[1].color=discord.Colour.from_rgb(rgb[0],rgb[1],rgb[2])
					emb[0]=True
				elif line.startswith("$addField["):
					emb[1].add_field(name=line[len("$addField["):].split(";")[0], value=line[len("$addField["):].split(";")[1], inline=True)
					emb[0]=True
				elif line.startswith("$thumbnail["):
					emb[1].set_thumbnail(url=line[len("$thumbnail["):])
					emb[0]=True
				elif line.startswith("$image["):
					emb[1].set_image(url=line[len("$image["):])
					emb[0]=True
				elif line.startswith("$footer["):
					emb[1].set_footer(text=line[len("$footer["):])
					emb[0]=True
				elif line.startswith("$author["):
					emb[1].set_author(name=line[len("$author["):])
					emb[0]=True
				elif line.startswith("$footerIcon["):
					if not isinstance(emb[1].footer.text, str):
						emb[1].set_footer(text="", icon_url=line[len("$footerIcon["):])
					else:
						emb[1].set_footer(text=emb[1].footer.text, icon_url=line[len("$footerIcon["):])
					emb[0]=True
				elif line.startswith("$authorIcon["):
					if not isinstance(emb[1].author.name, str):
						emb[1].set_author(name="", icon_url=line[len("$authorIcon["):])
					else:
						emb[1].set_author(name=emb[1].author.name, icon_url=line[len("$authorIcon["):])
					emb[0]=True
				elif line.startswith("$deletecommand"):
					await need[0].delete()
				elif line.startswith("$addReactions["):
					reactions = line[len("$addReactions["):].split(";")
				elif line.startswith("$addCmdReactions["):
					for react in line[len("$addCmdReactions["):].split(";"):
						await need[0].add_reaction(react)
				elif line.startswith("$addTimestamp"):
					emb[1].timestamp = datetime.datetime.utcnow()
					emb[0]=True
				elif line.startswith("$authorURL["):
					if not isinstance(emb[1].author.name, str):
						if not isinstance(emb[1].author.icon_url, str):
							emb[1].set_author(name="", url=line[len("$authorURL["):])
						else:
							emb[1].set_author(name="", icon_url=emb[1].author.icon_url, url=line[len("$authorURL["):])
					else:
						emb[1].set_author(name=emb[1].author.name, icon_url=emb[1].author.icon_url, url=line[len("$authorURL["):])
					emb[0]=True
				elif line.startswith("$suppressErrors["):
					error[1]=line[len("$suppressErrors["):]
					error[0]=False
				elif line.startswith("$embedSuppressErrors["):
					line = line[len("$embedSuppressErrors["):]
					error[0]="Embed"
					error[1]=line
				elif line.startswith("$addEmoji["):
					def bytes(image:Image):
						imgByteArr = io.BytesIO()
						image.save(imgByteArr, format=image.format)
						imgByteArr = imgByteArr.getvalue()
						return imgByteArr
					line = line[len("$addEmoji["):].split(";")
					emoji = await need[0].guild.create_custom_emoji(name=line[0], image = bytes(Image.open(io.BytesIO(requests.get(line[1]).content))))
					if len(line)>2:
						if line[2]=="yes":
							if binstr == "":
								binstr += f"<:{emoji.name}:{emoji.id}>"
							else:
								binstr += "\n"+f"<:{emoji.name}:{emoji.id}>"
			except Exception as e:
				if error[0]==True:
					await need[0].channel.send(f"❌Ошибка: `{e}`\nСтрока: {linec}\nЛиния: {reline}")
				else:
					if error[0]=="Embed":
						line = error[1].replace("%error%",str(e)).replace("%line%",str(linec)).replace("%text%",str(reline)).split(";")
						erremb = discord.Embed(title=line[0], description=line[1])
						if line[2]!="":
							rgb=list(int(line[2][i:i+2], 16) for i in (0, 2, 4))
							erremb.color=discord.Colour.from_rgb(rgb[0],rgb[1],rgb[2])
						if line[3]!="":
							erremb.set_author(name=line[3])
						if line[4]!="":
							erremb.set_footer(text=line[4], icon_url=line[5])
						await need[0].channel.send(embed=erremb)
					else:
						if error[1]!="":
							await need[0].channel.send(error[1].replace("%error%",str(e)).replace("%line%",str(linec)).replace("%text%",str(reline)))
		else:
			reline = reline.replace("$authorID",str(need[0].author.id))
			reline = reline.replace("$message",content)
			if binstr == "":
				binstr += reline
			else:
				binstr += "\n"+reline
	if emb[0]:
		msg = await need[0].channel.send(content=binstr,embed=emb[1])
	else:
		if binstr!="":
			msg = await need[0].channel.send(binstr)
	for react in reactions:
		try:
			await msg.add_reaction(react)
		except Exception as e:
			await need[0].channel.send(f"❌Ошибка, неудалось добавить реакцию {react}!")