functions = {"functions":{"$eval":"noarg","$title[":"arg","$description[":"arg","$color[":"arg","$addField[":"arg","$thumbnail[":"arg","$image[":"arg","$footer[":"arg","$author[":"arg","$authorIcon[":"arg","$footerIcon[":"arg","$deletecommand":"noarg","$addReactions[":"arg","$addCmdReactions[":"arg","$addTimestamp":"noarg","$authorURL[":"arg","$suppressErrors[":"arg","$embedSuppressErrors[":"arg","$addEmoji[":"arg","$textSplit[":"arg","$replyIn[":"arg","$nomention":"noarg", "$allowMention":"noarg"},"adds":{"$message":"noarg","$splitText[":"arg","$math[":"arg","$authorID":"noarg","$authorAvatar":"noarg","$allMembersCount":"noarg","$argCount[":"arg","$message[":"arg","$mentioned[":"arg","$noMentionMessage[":"arg","$noMentionMessage":"noarg","$getTextSplitLength":"noarg"}}
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
			code=info["code"]
		except Exception as e:
			for n in info:
				if not n in ["name","prefix","type"]:
					code.append(info[n])
		self._codes["commands"][self._count]["name"]=info["name"]
		func=[]
		funstr=""
		skob=0
		linec=0
		for fun in info["code"]:
			linec+=1
			if any(fun.startswith(func) for func in functions["functions"]):
				if skob>0:
					func.append(funstr)
					if linec==len(info["code"]):
						func.append(fun)
					else:
						try:
							if functions["functions"][fun]=="noarg":
								func.append(fun)
							else:
								funstr=fun
						except:
							funstr=fun
				elif skob==0:
					if linec==len(info["code"]):
						func.append(fun)
					else:
						try:
							if functions["functions"][fun]=="noarg":
								func.append(fun)
							else:
								funstr=fun
								skob+=1
						except:
							funstr=fun
							skob+=1
			elif fun.endswith("]") and skob>0:
				funstr+="/n"+fun
				func.append(funstr)
				funstr=""
				skob-=1
			else:
				if skob>0:
					funstr+="/n"+fun
				else:
					func.append(fun)
		code = func
		self._codes["commands"][self._count]["code"]=code
		try:
			self._codes["commands"][self._count]["prefix"]=info["prefix"]
		except:
			self._codes["commands"][self._count]["prefix"]=self._prefix
		try:
			self._codes["commands"][self._count]["type"]=info["type"]
		except:
			self._codes["commands"][self._count]["type"]="notself"

	def start(self):
		_start(self._client, self)

def _start(client, info):
	
	@client.event
	async def on_ready():
		print("Бот онлайн!")
	
	@client.event
	async def on_message(message):
		exe = True
		if exe:
			if info._type=="ping":
				def remember(text):
					global command
					command = text
					return True
				if any(message.content.startswith(info._codes["commands"][cmd]["prefix"]+info._codes["commands"][cmd]["name"]) and remember(cmd) for cmd in info._codes["commands"]):
					if info._codes["commands"][command]["type"]=="self":
						await use([message, command, "commands"],info)
					else:
						if message.author.id!=client.user.id:
							await use([message, command, "commands"],info)
			elif info._type=="all":
				for cmd in info._codes["commands"]:
					if message.content.startswith(info._codes["commands"][cmd]["prefix"]+info._codes["commands"][cmd]["name"]):
						if info._codes["commands"][cmd]["type"]=="self":
							await use([message, cmd, "commands"],info)
						else:
							if message.author.id!=client.user.id:
								await use([message, cmd, "commands"],info)
	if info._self:
		client.run(info._token, bot=False)
	else:
		client.run(info._token)

async def use(need, info):
	import discord
	import io
	import asyncio
	from PIL import Image
	import requests
	import datetime
	binstr = ""
	content = need[0].content[len(info._codes[need[2]][need[1]]["prefix"]+info._codes[need[2]][need[1]]["name"]):].lstrip(" ")
	emb = [False, discord.Embed()]
	lines = info._codes[need[2]][need[1]]["code"]
	reactions = []
	linec = 0
	error = [True,""]
	split = []
	if "$eval" in lines:
		lines=lines[:lines.index("$eval")]
		func = []
		funstr=""
		skob=0
		for fun in content.split("\n"):
			linec+=1
			if any(fun.startswith(func) for func in functions["functions"]):
				if skob>0:
					func.append(funstr)
					if linec==len(content.split("\n")):
						func.append(fun)
					else:
						try:
							if functions["functions"][fun]=="noarg":
								func.append(fun)
							else:
								funstr=fun
						except:
							funstr=fun
				elif skob==0:
					if linec==len(content.split("\n")):
						func.append(fun)
					else:
						try:
							if functions["functions"][fun]=="noarg":
								func.append(fun)
							else:
								funstr=fun
								skob+=1
						except:
							funstr=fun
							skob+=1
			elif fun.endswith("]") and skob>0:
				funstr+="/n"+fun
				func.append(funstr)
				funstr=""
				skob-=1
			else:
				if skob>0:
					funstr+="/n"+fun
				else:
					func.append(fun)
		lines=lines + func
	linec=0
	allow=True
	ment=str(need[0].author.mention)+"\n"
	if "$nomention" in lines:
		lines.remove("$nomention")
		ment=""
	if "$allowMention" in lines:
		lines.remove("$allowMention")
		allow=False
	for line in lines:
		linec+=1
		reline = line
		def remember(text):
			global function
			function = text
			return True
		if any(line.startswith(func) and remember(func) for func in functions["functions"]):
			reline = replaces([reline, info, content.replace("[","⦍").replace("]","⦎"), need, split, allow])
			line = reline
			if functions["functions"][function]=="arg":
				if line.endswith("]"):
					line=line[:-1]
			try:
				line=line.replace("/n","\n")
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
				elif line.startswith("$replyIn["):
					line = line[len("$replyIn["):]
					if line.endswith("s"):
						line=line.rstrip("s")
					elif line.endswith("m"):
						line=line.rstrip("m")
						line=int(line)*60
					elif line.endswith("h"):
						line=line.rstrip("h")
						line=int(line)*60*60
					elif line.endswith("d"):
						line=line.rstrip("d")
						line=int(line)*60*60*24
					await asyncio.sleep(int(line))
				elif line.startswith("$addEmoji["):
					def bytes(image:Image):
						imgByteArr = io.BytesIO()
						image.save(imgByteArr, format=image.format)
						imgByteArr = imgByteArr.getvalue()
						return imgByteArr
					line = line[len("$addEmoji["):].split(";")
					emoji = await need[0].guild.create_custom_emoji(name=line[0], image = bytes(Image.open(io.BytesIO(requests.get(line[1]).content)).convert("RGB")))
					if len(line)>2:
						if line[2]=="yes":
							if binstr == "":
								binstr += f"<:{emoji.name}:{emoji.id}>"
							else:
								binstr += "\n"+f"<:{emoji.name}:{emoji.id}>"
				elif line.startswith("$textSplit["):
					line = line[len("$textSplit["):].split(";")
					split = line[0].split(line[1])
				elif line.startswith("$useChannel[channelID]["):
					reactions = line[len("$addReactions["):].split(";")
				else:
					if binstr == "":
						binstr += line
					else:
						binstr += "\n"+line
			except Exception as e:
				if error[0]==True:
					await need[0].channel.send(f"❌Ошибка: `{e}`\nСтрока: {linec}\nЛиния: "+reline.replace("/n","\n"))
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
			reline = replaces([reline, info, content.replace("[","⦍").replace("]","⦎"), need, split, allow])
			if binstr == "":
				binstr += reline
			else:
				binstr += "\n"+reline
	binstr=binstr.replace("/n","\n")
	if emb[0]:
		msg = await need[0].channel.send(content=ment+binstr,embed=emb[1])
	else:
		if ment+binstr!="":
			msg = await need[0].channel.send(ment+binstr)
	for react in reactions:
		try:
			await msg.add_reaction(react)
		except Exception as e:
			await need[0].channel.send(f"❌Ошибка: `{e}`\nСтрока: {linec}\nЛиния: "+reline.replace("/n","\n"))

def replaces(info):
	import re
	reline = info[0]
	need = info[3]
	content = info[2]
	split = info[4]
	allow = info[5]
	info = info[1]
	nowloop = ""
	members = 0
	content = re.sub("\s\s+", " ", content)
	def in_replaces(info):
		reline = info[0]
		need = info[1]
		members = info[2]
		content = info[3]
		split = info[5]
		allow = info[6]
		info = info[4]
		reline = reline.replace("$authorID",str(need[0].author.id))
		reline = reline.replace("$authorAvatar",str(need[0].author.avatar_url))
		reline = reline.replace("$allMembersCount",str(members))
		reline = reline.replace("$getTextSplitLength",str(len(split)))
		recontent=content
		for guild in info._client.guilds:
			members += len(guild.members)
		for m in need[0].mentions:
			recontent=recontent.replace(str(m.mention).replace("!",""),"")
			if allow:
				content=content.replace(str(m.mention).replace("!",""), str(m.display_name))
		recontent=recontent.lstrip(" ")
		content=content.lstrip(" ")
		nowloop=""
		while "$message[" in reline:
			if nowloop==reline:
				break
			else:
				nowloop=reline
				try:
					reline=reline.replace("$message["+reline.split("$message[")[-1].split("]")[0]+"]", content.split(" ")[int(reline.split("$message[")[-1].split("]")[0])-1])
				except Exception as e:
					reline=reline.replace("$message["+reline.split("$message[")[-1].split("]")[0]+"]", "")
		reline = reline.replace("$message",content)
		while "$noMentionMessage[" in reline:
			if nowloop==reline:
				break
			else:
				nowloop=reline
				try:
					reline=reline.replace("$noMentionMessage["+reline.split("$noMentionMessage[")[-1].split("]")[0]+"]", recontent.split(" ")[int(reline.split("$noMentionMessage[")[-1].split("]")[0])-1])
				except Exception as e:
					reline=reline.replace("$noMentionMessage["+reline.split("$noMentionMessage[")[-1].split("]")[0]+"]", "")
		reline = reline.replace("$noMentionMessage",recontent)
		while "$mentioned[" in reline:
			if nowloop==reline:
				break
			else:
				nowloop=reline
				try:
					reline=reline.replace("$mentioned["+reline.split("$mentioned[")[-1].split("]")[0]+"]", str(need[0].mentions[int(reline.split("$mentioned[")[-1].split("]")[0])-1].id))
				except Exception as e:
					reline=reline.replace("$mentioned["+reline.split("$mentioned[")[-1].split("]")[0]+"]", "")
		return reline
	while "$splitText[" in reline:
		if nowloop==reline:
			break
		else:
			prereline=in_replaces([reline.split("$splitText[")[-1].split("]")[0], need, members, content, info, split, allow])
			nowloop=reline
			try:
				reline=reline.replace("$splitText["+reline.split("$splitText[")[-1].split("]")[0]+"]", str(split[int(prereline.split("$splitText[")[-1].split("]")[0])-1]))
			except Exception as e:
				reline=reline.replace("$splitText["+reline.split("$splitText[")[-1].split("]")[0]+"]", "")
	while "$argCount[" in reline:
		if nowloop==reline:
			break
		else:
			prereline=in_replaces([reline.split("$argCount[")[-1].split("]")[0], need, members, content, info, split, allow])
			nowloop=reline
			if prereline.split("$argCount[")[-1].split("]")[0].split(" ")[0]!="":
				reline=reline.replace("$argCount["+reline.split("$argCount[")[-1].split("]")[0]+"]", str(len(prereline.split("$argCount[")[-1].split("]")[0].split(" "))))
			else:
				reline=reline.replace("$argCount["+reline.split("$argCount[")[-1].split("]")[0]+"]", "0")
	while "$math[" in reline:
		if nowloop==reline:
			break
		else:
			prereline=in_replaces([reline.split("$math[")[-1].split("]")[0], need, members, content, info, split, allow])
			nowloop=reline
			try:
				reline=reline.replace("$math["+reline.split("$math[")[-1].split("]")[0]+"]", eval(prereline.split("$math[")[-1].split("]")[0],{'__builtins__':None}))
			except Exception as e:
				reline=reline.replace("$math["+reline.split("$math[")[-1].split("]")[0]+"]", "nan")
	reline=in_replaces([reline, need, members, content, info, split, allow])
	return reline