#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from encrypti0n.classes.config import *
from encrypti0n.classes import utils, rsa

# imports.
import base64, string, random
from Crypto.Cipher import AES as _AES_
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2

# the symetric aes 254 object class.
class AES(object):
	def __init__(self, passphrase=None):
		
		# check params.
		response = r3sponse.check_parameters({
			"passphrase:str":passphrase,})
		if not response.success: raise ValueError(response.error)

		# arguments.
		self.passphrase = passphrase

		# variables.
		self.block_size = 16
		self.pad = lambda s: s + (self.block_size - len(s) % self.block_size) * chr(self.block_size - len(s) % self.block_size)
		self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]
		
	def encrypt(self, raw):
		if raw in ["", b"", None, False]:
			return r3sponse.error_response("Can not encrypt null data.")
		response = self.get_key()
		if not r3sponse.success(response): return response
		key = response["key"]
		salt = response["salt"]
		if isinstance(raw, bytes):
			raw = raw.decode()
		raw = self.pad(raw)
		iv = Random.new().read(_AES_.block_size)
		cipher = _AES_.new(key, _AES_.MODE_CBC, iv)
		encrypted = base64.b64encode(iv + salt + cipher.encrypt(raw.encode()))
		if raw != b"" and encrypted == b"":
			return r3sponse.error_response("Failed to encrypt the specified data with the current passphrase / salt.")
		return r3sponse.success_response("Successfully encrypted the specified data.", {
			"encrypted":encrypted,
		})
	def decrypt(self, enc):
		if enc in ["", b"", None, False]:
			return r3sponse.error_response("Can not decrypt null data.")
		if isinstance(enc, str):
			enc = enc.encode()
		enc = base64.b64decode(enc)
		iv_salt = enc[:32]
		iv = iv_salt[:16]
		salt = iv_salt[16:]
		response = self.get_key(salt=salt)
		if not r3sponse.success(response): return response
		key = response["key"]
		cipher = _AES_.new(key, _AES_.MODE_CBC, iv)
		decrypted = self.unpad(cipher.decrypt(enc[32:]))
		if enc != b"" and decrypted == b"":
			return r3sponse.error_response("Failed to decrypt the specified data with the current passphrase / salt.")
		return r3sponse.success_response("Successfully decrypted the specified data.", {
			"decrypted":decrypted,
		})
	def get_key(self, salt=None):
		if salt == None:
			salt = self.generate_salt()["salt"]
		if isinstance(salt, str):
			salt = salt.encode()
		kdf = PBKDF2(self.passphrase, salt, 64, 1000)
		key = kdf[:32]
		return r3sponse.success_response("Successfully loaded the aes key.", {
			"key":key,
			"salt":salt,
		})
	def generate_salt(self):
		length=16
		chars = ''.join([string.ascii_uppercase, string.ascii_lowercase, string.digits])
		salt = ''.join(random.choice(chars) for x in range(length))
		return r3sponse.success_response("Successfully generated a salt.", {
			"salt":salt,
		})

# the asymmetric aes 254 object class.
class AsymmetricAES(object):
	def __init__(self,
		# the public key (str).
		public_key=None,
		# the private key (str).
		private_key=None,
		# the key passphrase (str / null).
		passphrase=None,
		# enable memory when the keys are not saved.
		memory=False,
	):
		self.rsa = rsa.RSA(public_key=public_key, private_key=private_key, passphrase=passphrase, memory=memory)
	def generate_keys(self):
		return self.rsa.generate_keys()
	def edit_passphrase(self, passphrase=None):
		return self.rsa.edit_passphrase(passphrase=passphrase)
	def load_keys(self):
		return self.rsa.load_keys()
	def load_private_key(self):
		return self.rsa.load_private_key()
	def load_public_key(self):
		return self.rsa.load_public_key()
	def encrypt(self, string, decode=False):
		if isinstance(string, bytes):
			string = string.decode()
		
		# encrypt data with aes.
		passphrase = utils.__generate_shell_string__(characters=64, numerical_characters=True)
		aes = AES(passphrase=passphrase)
		response = aes.encrypt(string)
		if not r3sponse.success(response): return response
		aes_encrypted = response["encrypted"]
		if b" " in aes_encrypted:
			return r3sponse.error_response("AES encrypt data contains invalid ' ' character(s).")

		# encrypt aes key with rsa.
		response = self.rsa.encrypt_string(passphrase, decode=False)
		if not r3sponse.success(response): return response
		rsa_encrypted = response["encrypted"]

		# pack encrypted.
		encrypted = rsa_encrypted+b" "+aes_encrypted

		# success.
		if decode: encrypted = encrypted.decode()
		return r3sponse.success_response("Successfully encrypted the specified data.", {
			"encrypted":encrypted
		})

		#
	def decrypt(self, string, decode=False):

		# split encrypted aes key.
		if isinstance(string, bytes):
			string = string.decode()
		try:
			key,encrypted = string.split(" ")
		#except:
		except KeyboardInterrupt:
			return r3sponse.error_response("Unable to unpack the encrypted data.")

		# decypt key with rsa.
		response = self.rsa.decrypt_string(key, decode=False)
		if not r3sponse.success(response): return response
		passphrase = response["decrypted"].decode()

		# decrypt with aes.
		aes = AES(passphrase=passphrase)
		response = aes.decrypt(encrypted)
		if not r3sponse.success(response): return response
		decrypted = response["decrypted"]

		# success.
		if decode: decrypted = decrypted.decode()
		return r3sponse.success_response("Successfully decrypted the specified data.", {
			"decrypted":decrypted
		})

		#
	def encrypt_file(self, input=None, output=None, remove=False, base64_encoding=False):
		

		# check params.
		response = r3sponse.check_parameters({
			"input":input,
			"output":output,})
		if not r3sponse.success(response): return response

		# encrypt.
		data = utils.__load_bytes__(input)
		if base64_encoding:
			data = base64.b64encode(data)
		response = self.encrypt(data, decode=False)
		if not r3sponse.success(response): return response

		# write out.
		try: utils.__save_bytes__(output, response["encrypted"])
		except: return r3sponse.success_response(f"Failed to write out encrypted file {output}.")

		# remove.
		if remove and input != output: 
			try: os.remove(input)
			except PermissionError: os.system(f"sudo rm -fr {input}")

		# handler.
		return r3sponse.success_response(f"Successfully encrypted file {input} to {output}.")

		#
	def decrypt_file(self, input=None, output=None, remove=False, base64_encoding=False):
		

		# check params.
		response = r3sponse.check_parameters({
			"input":input,
			"output":output,})
		if not r3sponse.success(response): return response

		# encrypt.
		response = self.decrypt(utils.__load_bytes__(input), decode=False)
		if not r3sponse.success(response): return response

		# write out.
		decrypted = response.decrypted
		if base64_encoding:
			decrypted = base64.b64decode(decrypted)
		try: utils.__save_bytes__(output, decrypted)
		except: return r3sponse.success_response(f"Failed to write out decrypted file {output}.")

		# remove.
		if remove and input != output: 
			try: os.remove(input)
			except PermissionError: os.system(f"sudo rm -fr {input}")

		# handler.
		return r3sponse.success_response(f"Successfully decrypted file {input} to {output}.")

		#
	def encrypt_directory(self, input=None, output=None, remove=False):

		# checks.
		file_path = Formats.FilePath(input)
		if not file_path.exists():
			return r3sponse.error_response(f"Directory [{input}] does not exist.")
		if not file_path.directory():
			return r3sponse.error_response(f"Directory path [{input}] is not a directory.")

		# zip path.
		if output == None:
			if input[len(input)-1] == "/": zip_path = input[:-1]
			else: zip_path = str(input)
			zip_path = f'{zip_path}.enc.zip'
		elif ".enc.zip" not in output:
			return r3sponse.error_response(f"Invalid output format [{output}], the format must end with [***.enc.zip]")
		else:
			zip_path = output

		# check output.
		if os.path.exists(zip_path):
			return r3sponse.error_response(f"output path [{zip_path}] already exists.")

		# create zip.
		zip = Files.Zip(path=zip_path)
		zip.create(source=input)

		# encrypt zip.
		response = self.encrypt_file(input=zip.file_path.path, output=zip.file_path.path, remove=False, base64_encoding=True)
		if response.success and os.path.exists(zip.file_path.path) :
			if remove and input != output:
				try: 
					os.system(f"rm -fr {input}")
					if os.path.exists(input): raise PermissionError("")
				except PermissionError: os.system(f"sudo rm -fr {input}")
			return r3sponse.success_response(f"Successfully encrypted directory [{input}].")
		else:
			zip.file_path.delete(forced=True)
			return r3sponse.error_response(f"Failed to encrypt directory [{input}].")

		#
	def decrypt_directory(self, input=None, output=None, remove=False):

		# checks.
		file_path = Formats.FilePath(input)
		if not file_path.exists():
			return r3sponse.error_response(f"Input [{input}] does not exist.")
		if file_path.directory():
			return r3sponse.error_response(f"Input path [{input}] is a directory.")

		# dir path.
		if output == None:
			if ".enc.zip" not in input:
				return r3sponse.error_response(f"Invalid input format [{input}], the format must end with [***.enc.zip]")
			dir_path = output.replace(".enc.zip", "/").replace("//","/").replace("//","/").replace("//","/")
		else:
			if ".enc.zip" in output:
				return r3sponse.error_response(f"Invalid output format [{output}], the format can not end with [***.enc.zip]")
			dir_path = output.replace(".enc.zip", "/")

		# check output.
		l_dir_path = dir_path
		if l_dir_path[len(l_dir_path)-1] == "/": l_dir_path = l_dir_path[:-1]
		if os.path.exists(l_dir_path):
			return r3sponse.error_response(f"Output path [{l_dir_path}] already exists.")
		
		# decrypt zip.
		tmp_zip = f"/tmp/{Formats.FilePath(input).name()}"
		if os.path.exists(tmp_zip): os.system(f"rm -fr {tmp_zip}")
		response = self.decrypt_file(input=input, output=tmp_zip, remove=False, base64_encoding=True)
		if not response.success:
			return r3sponse.error_response(f"Failed to decrypted directory [{input}], error: {response.error}")

		# extract zip.
		tmp_extract = f"/tmp/{Formats.String('').generate(length=32,capitalize=True,digits=True)}/"
		if os.path.exists(tmp_extract): os.system(f"rm -fr {tmp_extract}")
		os.mkdir(tmp_extract)
		zip = Files.Zip(path=tmp_zip)
		zip.extract(base=tmp_extract)
		paths = Files.Directory(path=tmp_extract).paths()
		if len(paths) == 1:
			os.system(f"mv {paths[0]} {output}")
			if os.path.exists(output):
				os.system(f"rm -fr {tmp_extract}")
				os.system(f"rm -fr {tmp_zip}")
				if remove and input != output:
					try: os.remove(input)
					except PermissionError: os.system(f"sudo rm -fr {input}")
				return r3sponse.success_response(f"Successfully decrypted directory [{input}].")
			else:
				os.system(f"rm -fr {tmp_extract}")
				os.system(f"rm -fr {tmp_zip}")
				return r3sponse.error_response(f"Failed to decrypt directory [{input}].")
		else:
			os.system(f"rm -fr {tmp_extract}")
			os.system(f"rm -fr {tmp_zip}")
			return r3sponse.error_response(f"Failed to decrypt directory [{input}].")

		#

# the aes database object class.
class Database(object):
	def __init__(self,
		# the aes object class.
		aes=None,
		# the root path of the database.
		path=None,
	):

		# check params.
		response = r3sponse.check_parameters({
			"aes:object":aes,
			"path:str":path,})
		if not response.success: raise ValueError(response.error)

		# arguments.
		self.aes = aes
		self.path = f"{utils.__clean_url__(path, strip_first=False, strip_last=True, remove_double_slash=True)}/"
		if not os.path.exists(self.path[:-1]): 
			os.mkdir(self.path)
			os.system(f"chown {OWNER}:{GROUP} {self.path} && chmod 770 {self.path}")

		# variables.
		self.activated = False

		#
	def activate(self):

		# check sample.
		if not os.path.exists(f"{self.path}.passphrase"):
			response = self.aes.encrypt(self.aes.rsa.passphrase)
			if not response.success: return response
			try: utils.__save_bytes__(f"{self.path}.passphrase", response.encrypted)
			except: return r3sponse.error_response(f"Failed to write out encrypted passphrase {self.path}.passphrase")
		else:
			try: passphrase = utils.__load_bytes__(f"{self.path}.passphrase")
			except: return r3sponse.error_response(f"Failed to load encrypted passphrase {self.path}.passphrase")
			response = self.aes.decrypt(passphrase)
			if not response.success: return response
			if response.decrypted.decode().replace("\n","") != self.aes.rsa.passphrase.replace("\n",""):
				return r3sponse.error_response("Specified an incorrect passphrase.")

		# success.
		self.activated = True
		return r3sponse.success_response(f"Successfully activated encrypted database {self.path}.")

		#
	def check(self, 
		# the subpath of the content (! param number 1).
		path=None, 
		# the default content data (! param number 2).
		default=None,
		# save the changes.
		save=True,
	):
		if not self.activated: return r3sponse.error_response(f"Encrypted database {self.path} is not activated yet, call database.activate() first.")
		response = r3sponse.check_parameters({
			"path:str":path,
			"default:str,dict,list,int,float":default,
			"save:bool":save,})
		if not response.success: return response
		content = self.DataObject(path=f"{self.path}/{path}", aes=self.aes)
		response = content.check(default=default, save=save)
		if not response.success: return response
		return r3sponse.success_response(f"Successfully checked content {path}.", {
			"content":content,
		})
	def load(self, 
		# the subpath of the content (! param number 1).
		path=None, 
	):
		if not self.activated: return r3sponse.error_response(f"Encrypted database {self.path} is not activated yet, call database.activate() first.")
		response = r3sponse.check_parameters({
			"path:str":path,})
		if not response.success: return response
		content = self.DataObject(path=f"{self.path}/{path}", aes=self.aes)
		response = content.load()
		if not response.success: return response
		return r3sponse.success_response(f"Successfully loaded content {path}.", {
			"content":content,
		})
	def save(self, 
		# the content object (! param number 1).
		content=None,
	):
		if not self.activated: return r3sponse.error_response(f"Encrypted database {self.path} is not activated yet, call database.activate() first.")
		response = r3sponse.check_parameters({
			"content:object":content,})
		if not response.success: return response
		response = content.save()
		if not response.success: return response
		return r3sponse.success_response(f"Successfully saved content {path}.")
	
	# a data object.
	class DataObject(object):
		def __init__(self, 
			# the path.
			path=None, 
			# the default data, specify to call self.check() automatically.
			default=None,
			# the aes object.
			aes=None,
		):
			self.path = f"{utils.__clean_url__(path, strip_first=False, strip_last=True, remove_double_slash=True)}"
			self.aes = aes
			self.base = Formats.FilePath(path).base()
			self.content = None
			self.format = None
			self.loaded = False
			if default != None:
				response = self.check(default=default, save=True)
				if not response.success: raise ValueError(response.error)
		# check the content.
		def check(self, default=None, save=True):
			response = r3sponse.check_parameters({
				"default:dict,list,str,float,int":default,
				"save:bool":save,})
			if not r3sponse.success(response): return response
			if not os.path.exists(self.base): os.system(f"mkdir -p {self.base}")
			do = False
			if not os.path.exists(self.path): 
				do = True
				new = default
			else:
				response = self.load()
				if not r3sponse.success(response): return response
				old_format = Formats.get(self.content, serialize=True)
				new_format = Formats.get(default, serialize=True)
				if old_format != new_format:
					return r3sponse.error_response(f"Mismatching formats, old format: {old_format}, new format: {new_format}.")
				if new_format == "dict":
					old = dict(self.content)
					new = Files.Dictionary(path=False, dictionary=old).check(default=default, save=False)
					if dict(new) != dict(old): do = True
				elif new_format == "list":
					old = list(self.content)
					new = list(default)
					for i in default:
						new.append(i)
					if new != old: do = True
				elif new_format in ["str", "float", "int"]:
					old = str(self.content)
					new = str(default)
					if new != old: do = True
				else: return r3sponse.error_response(f"Unsupported new format: {new_format}.")
			if do:
				self.content = new
				self.format = Formats.get(self.content, serialize=True)
				if save:
					self.loaded = True
					response = self.save()
					if not response.success: return response
			return r3sponse.success_response(f"Successfully checked the content of {self.path}.")
		# load & decrypt.
		def load(self):
			try:
				content = utils.__load_file__(self.path)
			except Exception as e: return r3sponse.error_response(f"Failed to load content {self.path}, {e}.")
			format, content = content.split(" ")
			response = self.aes.decrypt(content.encode())
			if not response.success: return response
			decrypted = response.decrypted.decode()
			if format in ["dict", "list"]:
				try:
					content = json.loads(decrypted)
				except Exception as e: return r3sponse.error_response(f"Failed to serialize content {self.path}, {e}.")
			elif format in ["int"]:
				try:
					content = int(decrypted)
				except Exception as e: return r3sponse.error_response(f"Failed to serialize content {self.path}, {e}.")
			elif format in ["float"]:
				try:
					content = float(decrypted)
				except Exception as e: return r3sponse.error_response(f"Failed to serialize content {self.path}, {e}.")
			elif format in ["str"]:
				try:
					content = str(decrypted)
				except Exception as e: return r3sponse.error_response(f"Failed to serialize content {self.path}, {e}.")
			else: return r3sponse.error_response(f"Unsupported format: {format}.")
			self.content = content
			self.format = format
			self.loaded = True
			return r3sponse.success_response(f"Successfully loaded content {self.path}.")
		# save & encrypt.
		def save(self):
			if not self.loaded:
				return r3sponse.error_response("The data object is not loaded yet, you must call content.load() first.")
			if self.format in ["list", "dict"]:
				try:
					content = json.dumps(self.content)
				except Exception as e: return r3sponse.error_response(f"Failed to dump content {self.path}, {e}.")
			elif self.format in ["str", "int", "float"]:
				content = str(self.content)
			else:
				raise ValueError(f"DataObject with format {self.format} does not support the <self.save()> function.")
			response = self.aes.encrypt(content)
			if not response.success: return response
			try:
				content = utils.__save_bytes__(self.path, f"{self.format} ".encode()+response.encrypted)
			except Exception as e: return r3sponse.error_response(f"Failed to save content {self.path}, {e}.")
			return r3sponse.success_response(f"Successfully saved content {self.path}.")
		# iterate over self keys & variables.
		def items(self):
			if not self.loaded: raise ValueError("Load the content object first.")
			if self.format in ["list"]:
				return self.content
			elif self.format in ["dict"]:
				return self.content.items()
			else:
				raise ValueError(f"DataObject with format {self.format} does not support the <self.items()> function.")
		def keys(self):
			if not self.loaded: raise ValueError("Load the content object first.")
			if self.format in ["list"]:
				return self.content
			elif self.format in ["dict"]:
				return list(self.content.keys())
			else:
				raise ValueError(f"DataObject with format {self.format} does not support the <self.keys()> function.")
		def values(self):
			if not self.loaded: raise ValueError("Load the content object first.")
			if self.format in ["dict"]:
				return list(self.content.values())
			else:
				raise ValueError(f"DataObject with format {self.format} does not support the <self.values()> function.")
		def dict(self, serialize=False):
			if not self.loaded: raise ValueError("Load the content object first.")
			if self.format in ["dict"]:
				
				dictionary = {}
				for key, value in self.content.items():
					if serialize:
						if isinstance(value, object):
							value = str(value)
						elif value == "True": value = True
						elif value == "False": value = False
						elif value == "None": value = None
					dictionary[key] = value
				return dictionary
			else:
				raise ValueError(f"DataObject with format {self.format} does not support the <self.dict()> function.")
		# assign self variables by dictionary.
		def assign(self, dictionary):
			if not self.loaded: raise ValueError("Load the content object first.")
			if not isinstance(dictionary, dict):
				raise TypeError("You can only self assign with a dictionary as parameter.")
			if self.format in ["dict"]:
				for key,value in dictionary.items():
					self.content[key] = value
			else:
				raise ValueError(f"DataObject with format {self.format} does not support the <self.assign()> function.")
		# count items.
		def __len__(self):
			if not self.loaded: raise ValueError("Load the content object first.")
			if self.format in ["list"]:
				return len(self.content)
			elif self.format in ["dict"]:
				return len(self.content.keys())
			elif self.format in ["str", "int", "float"]:
				return len(str(self.content))
			else:
				return f"<encrypti0n.aes.Database.DataObject {self.path} content: {self.content}>"
		# support item assignment.
		def __setitem__(self, key, value):
			if not self.loaded: raise ValueError("Load the content object first.")
			if self.format in ["dict"]:
				setattr(self.content, key, value)
			else:
				raise ValueError(f"DataObject with format {self.format} does not support the self[""] item assignment.")
		def __getitem__(self, key):
			if not self.loaded: raise ValueError("Load the content object first.")
			if self.format in ["dict"]:
				return getattr(self.content, key)
			else:
				raise ValueError(f"DataObject with format {self.format} does not support the self[""] item assignment.")
		def __delitem__(self, key):
			if not self.loaded: raise ValueError("Load the content object first.")
			if self.format in ["dict"]:
				delattr(self.content, key)
			else:
				raise ValueError(f"DataObject with format {self.format} does not support the self[""] item assignment.")
		# string format.
		def __str__(self):
			if not self.loaded: 
				return f"<encrypti0n.aes.Database.DataObject {self.path} content: not loaded yet>"
			elif self.format in ["dict"]:
				return f"<encrypti0n.aes.Database.DataObject {self.path} content: {self.dict(serialize=True)}>"
			else:
				return f"<encrypti0n.aes.Database.DataObject {self.path} content: {self.content}>"
		def json(self,):
			if not self.loaded: raise ValueError("Load the content object first.")
			if self.format in ["dict"]:
				return self.dict(serialize=True)
			else:
				raise ValueError(f"DataObject with format {self.format} does not support the <self.json()> function.")

"""



# initialize.
aes = AES(passphrase="SomePassphrase12345!?")
database = Database(
	path="/tmp/database.enc",
	aes=aes,)

# activate the database.
response = database.activate()

# check data, dict or list.
response = database.check("users/vandenberghinc", {
	"Hello":"World"
})

# load data.
response = database.load("users/vandenberghinc")
content = response.content

# save data.
content.format # dict
content["Hello"] = "World!"
response = database.save(content)

# int & float data.
response = database.check("someint", 1500)
content = response.content
content.format # int
content.content = 1501
response = database.save(content)

# string data.
response = database.check("somestring", "Hello World")
content = response.content
content.format # str
content.content = "Hello World!"
response = database.save(content)





# initialize. 
aes = AES(passphrase="SomePassphrase12345!?")
aes.salt
 
# encrypt message
encrypted = aes.encrypt("This is a secret message".encode())
print(encrypted)
 
# decrypt using password
decrypted = aes.decrypt(encrypted)
print(decrypted)
"""