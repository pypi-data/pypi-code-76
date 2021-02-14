#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# insert the package for universal imports.
import os, sys, syst3m

# settings.
SOURCE_PATH = syst3m.defaults.get_source_path(__file__, back=1)
BASE = syst3m.defaults.get_source_path(SOURCE_PATH)
OS = syst3m.defaults.check_operating_system(supported=["linux", "osx"])
sys.path.insert(1, BASE)

# imports.
from encrypti0n.classes.config import *
from encrypti0n.classes import utils
#from encrypti0n.classes.rsa import RSA,EncryptedDictionary
from encrypti0n.classes.aes import AsymmetricAES


# the cli object class.
class CLI(cl1.CLI):
	def __init__(self):
		
		# cli.
		cl1.CLI.__init__(self,
			modes={
				"--encrypt /path/to/input /path/to/output [optional: --remove]":"Encrypt the provided file path.",
				"--decrypt /path/to/input /path/to/output [optional: --remove]":"Decrypt the provided file path.",
				"--encrypt-env . [optional: --remove]":"Encrypt the specified enviroment (automatically fills: --key ./key --input ./data/ --output ./data.enc.zip).",
				"--decrypt-env . [optional: --remove]":"Decrypt the specified enviroment (automatically fills: --key ./key --input ./data.enc.zip --output ./data/).",
				"--generate-keys":"Generate a key pair.",
				"--generate-passphrase [optional: --length 32]":"Generate a passphrase.",
				"--generate-aes [optional: --length 64]":"Generate an aes passphrase.",
				"-h / --help":"Show the documentation.",
			},
			options={
				"--remove":"Remove the input file.",
				"--key /path/to/directory/":"Specify the path to the key's directory.",
				"--public-key /path/to/directory/public_key":"Specify the path to the public key.",
				"--private-key /path/to/directory/private_key":"Specify the path to the private key.",
				"-p / --passphrase 'Passphrase123!'":"Specify the key's passphrase.",
			},
			executable=__file__,
			alias=ALIAS,)

		#
	def start(self):
		
		# help.
		if self.argument_present('-h') or self.argument_present('--help'):
			print(self.documentation)

		# encrypt.
		elif self.argument_present('--encrypt'):
			input = self.get_argument('--encrypt', index=1)
			output = self.get_argument('--encrypt', index=2)
			encryption = self.get_encryption(prompt_passphrase=False)
			response = encryption.load_public_key()
			r3sponse.log(response=response)
			if not r3sponse.success(response): sys.exit(1)
			if os.path.isdir(input): 
				response = encryption.encrypt_directory(input=input, output=output, remove=self.argument_present("--remove"))
			else: 
				response = encryption.encrypt_file(input=input, output=output, remove=self.argument_present("--remove"))
			r3sponse.log(response=response)

		# decrypt.
		elif self.argument_present('--decrypt'):
			input = self.get_argument('--decrypt', index=1)
			output = self.get_argument('--decrypt', index=2)
			encryption = self.get_encryption()
			response = encryption.load_private_key()
			r3sponse.log(response=response)
			if not r3sponse.success(response): sys.exit(1)
			if os.path.isdir(input) or (".enc.zip" in input and ".enc.zip" not in output): 
				response = encryption.decrypt_directory(input=input, output=output, remove=self.argument_present("--remove"))
			else: 
				response = encryption.decrypt_file(input=input, output=output, remove=self.argument_present("--remove"))
			r3sponse.log(response=response)

		# encrypt env.
		elif self.argument_present('--encrypt-env'):
			env = self.get_argument('--encrypt-env')
			key = f"{env}/key/".replace("//","/").replace("//","/").replace("//","/")
			input = f"{env}/data/".replace("//","/").replace("//","/").replace("//","/")
			output = f"{env}/data.enc.zip".replace("//","/").replace("//","/").replace("//","/")
			encryption = self.get_encryption(prompt_passphrase=False, key=key)
			response = encryption.load_public_key()
			r3sponse.log(response=response)
			if not r3sponse.success(response): sys.exit(1)
			response = encryption.encrypt_directory(input=input, output=output, remove=self.argument_present("--remove"))
			r3sponse.log(response=response)

		# decrypt env.
		elif self.argument_present('--decrypt-env'):
			env = self.get_argument('--decrypt-env')
			key = f"{env}/key/".replace("//","/").replace("//","/").replace("//","/")
			input = f"{env}/data.enc.zip".replace("//","/").replace("//","/").replace("//","/")
			output = f"{env}/data/".replace("//","/").replace("//","/").replace("//","/")
			encryption = self.get_encryption(key=key)
			response = encryption.load_private_key()
			r3sponse.log(response=response)
			if not r3sponse.success(response): sys.exit(1)
			response = encryption.decrypt_directory(input=input, output=output, remove=self.argument_present("--remove"))
			r3sponse.log(response=response)

		# generate-keys.
		elif self.argument_present('--generate-keys'):
			encryption = self.get_encryption(check_passphrase=True)
			response = encryption.generate_keys()
			r3sponse.log(response=response)

		# generate-aes.
		elif self.argument_present('--generate-aes'):
			print(f"Generated AES Passphrase: {utils.__generate__(length=int(self.get_argument('--length', required=False, empty=64)), capitalize=True, digits=True)}")

		# generate passphrase.
		elif self.argument_present('--generate-passphrase'):
			
			print("Generated passphrase:",Formats.String("").generate(length=length, capitalize=True, digits=True))

		# invalid.
		else: 
			print(self.documentation)
			print("Selected an invalid mode.")

		#
	def get_encryption(self, prompt_passphrase=True, check_passphrase=False, key=None):
		# key.
		public_key = self.get_argument('--public-key', required=False)
		private_key = self.get_argument('--private-key', required=False)
		if public_key == None and private_key == None:
			if key == None: key = self.get_argument('--key', required=True)
			public_key = f"{key}/public_key"
			private_key = f"{key}/private_key"
		# passphrase.
		passphrase = None
		if prompt_passphrase:
			passphrase = self.get_argument('-p', required=False)
			if passphrase == None:
				passphrase = self.get_argument('--passphrase', required=False)
			if passphrase == None:
				passphrase = utils.__prompt_password__("Enter the key's passphrase (leave blank to use no passphrase):")
				if check_passphrase and passphrase != utils.__prompt_password__("Enter the same passphrase:"):
					print("Error: passphrases do not match.")
					sys.exit(1)
			if passphrase in ["", "none", "null"]: passphrase = None
		# encryption.
		return AsymmetricAES(
			public_key=public_key,
			private_key=private_key,
			passphrase=passphrase,)
	
# main.
if __name__ == "__main__":
	cli = CLI()
	cli.start()
