# -*- coding: utf-8 -*-

import base64
import json
import os

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

from tailer_sdk import tailer_config


# Globals
#
TAILER_PRIVATE_KEY = "tailer_private_key.pem"
TAILER_PUBLIC_KEY = "tailer_public_key.pem"


def generate_key_pair():

    tailer_home_path = tailer_config.get_tailer_home()

    key = RSA.generate(2048)
    private_key = key.export_key()
    privatekey_filename = tailer_home_path + TAILER_PRIVATE_KEY
    file_out = open(privatekey_filename, "wb")
    file_out.write(private_key)
    print("Tailer Private key generated : %s" % privatekey_filename)

    public_key = key.publickey().export_key()
    publickey_filename = tailer_home_path + TAILER_PUBLIC_KEY
    file_out = open(publickey_filename, "wb")
    file_out.write(public_key)
    print("Tailer Public key generated : %s" % publickey_filename)


def encrypt_payload(payload):

    # Check if payload is a file
    #
    try:
        if os.path.isfile(payload) is True:
            with open(payload, "r")as file:
                payload = file.read()
    except Exception as ex:
        print(ex)


    # Get Tailer Home path
    #
    tailer_home_path = tailer_config.get_tailer_home()

    # Public Key
    #
    public_key_path = tailer_home_path + TAILER_PUBLIC_KEY
    print("Tailer Public key : " + public_key_path)
    public_key = RSA.import_key(open(public_key_path).read())

    # Convert MESSAGE to base64
    #
    base64_message = base64.b64encode((payload).encode('utf-8'))
    # print("Message         : " + payload)
    # print("BASE 64 message : " + str(base64_message))

    # Encrypt DATA
    #
    session_key = get_random_bytes(16)
    cipher_aes = AES.new(session_key, AES.MODE_EAX)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(public_key)

    # Encrypt the data with the AES session key
    ciphertext, tag = cipher_aes.encrypt_and_digest(base64_message)
    enc_session_key = (cipher_rsa.encrypt(session_key))

    output_data = {}
    output_data["cipher_aes"] = cipher_aes.nonce.hex()
    output_data["tag"] = tag.hex()
    output_data["ciphertext"] = ciphertext.hex()
    output_data["enc_session_key"] = enc_session_key.hex()

    print("\n\nCopy this JSON value as your secret in your configuration file :\n\n")
    print(json.dumps(output_data))
    print()