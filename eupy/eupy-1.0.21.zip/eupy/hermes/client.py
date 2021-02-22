#!/usr/bin/env python
import os
from email.mime.text import MIMEText
from pathlib import Path
from datetime import datetime
from time import sleep
import smtplib, ssl, imaplib, email
import subprocess, os
from getpass import getpass, getuser
import socket

class gmail:

  _port = 465
  _smtp_server = "smtp.gmail.com"
  _hostname    = socket.gethostname()
  _cachePath   = "{}/.config/hermes".format(str(Path.home()))
  _cacheFile   = "pass.txt"

  def __init__(self, receiver, cred=[], cache=True):

    assert receiver != "", "Receiver mail field is empty"
    cach_creds = self._searchCacheOrUpdate(cred, cache)
    self._username, self._password = cach_creds[0], cach_creds[1]
    self._receiver = receiver
    return

  ## Search cache for existing credentials. If found, check if newer are given
  def _searchCacheOrUpdate(self, cred, cache):
    creds = []
    ## If credentials are found in cache get them
    if os.path.isfile("{}/{}".format(self._cachePath, self._cacheFile)):
      with open("{}/{}".format(self._cachePath, self._cacheFile), 'r') as pf:
        creds = pf.read().splitlines()
        assert len(creds) == 2, "Cached credentials have wrong format!"
        assert creds[0] != "" and creds[1] != "", "Username or password field is empty"
      ## Given credentials are considered fresher than cached
      if len(cred) == 2 and creds != cred:
        creds = cred
        ## Write to cache, if instructed
        if cache:
          self._writeCache(creds)
    ## Otherwise use the given ones, if given
    else:
      creds.append(input("Sender email username: "))
      creds.append(str(getpass("Password: ")))
      ## Write to cache, if instructed
      if cache:
        self._writeCache(creds)
    return creds

  ## Update mail credentials to cache
  def _writeCache(self, cred):
    if not os.path.isdir(self._cachePath):
      os.makedirs(self._cachePath)
    with open("{}/{}".format(self._cachePath, self._cacheFile), 'w') as pf:
      pf.write("\n".join(cred))
    return

  ## Return username allocated to self object
  def user(self):
    return self._username

  ## Core function to broadcast a message to receiver
  def send_message(self, reporting_module, msg, request_reply = False):

    if self._password == "":
      assert False, "SMTP Server password for {} not specified!".format(self._username)

    message = self.create_message(reporting_module, msg)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(self._smtp_server, self._port, context=context) as server:
      server.login(self._username, self._password)
      server.sendmail(self._username, self._receiver, message.as_string())

    if request_reply:
      self._mailbox_check_wait(message)
      cmd = self._receive_instruction()
      self._execute_instructions(cmd)
      return cmd

    return

  ## MIME message constructor
  def create_message(self, rm, m):
    message = MIMEText("{}\n---------------------------------------\n\nReported by mail agent".format(m))
    message['Subject'] = "{}:{}".format(self._hostname, rm)
    message['From'] = self._username
    message['To'] = self._receiver
    message['Sent'] = str(datetime.now())
    return message

  ## Fetch mail, extract the body of the message and parse the instruction given
  def _receive_instruction(self):

    r, d = self._fetch_mail(encoding = "(UID BODY[TEXT])")
    msg = self._extract_email(d).as_string().split('\n')
    command = []

    for line in msg:
      if "$cmd" in line:
        command_str = ":".join(line.split(':')[1:])
        command = [x.split() for x in command_str.split(';') if x]
        break

    assert len(command) != 0, "Command field not extracted successfully!"
    return command

  ## Simple routine to execute in bash the instruction given
  def _execute_instructions(self, cmd):

    for c in cmd:
      proc = subprocess.Popen(c, stdout=subprocess.PIPE)
      out, err = proc.communicate()
      ## Convert to logger
      print(out.decode("utf-8"))
    return

  ## Busy waiting for a reply from a specific recipient
  def _mailbox_check_wait(self, message):

    r, d = self._fetch_mail()
    msg = self._extract_email(d)

    ## TODO add time too
    while not (message['Subject'] in msg['Subject'] and message['To'] in msg['From']):
      sleep(10)
      r, d = self._fetch_mail()
      msg = self._extract_email(d)
    return

  ## Login to mailbox and fetch the latest email
  def _fetch_mail(self, encoding = "(RFC822)"):

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(self._username, self._password)
    mail.list()

    # Out: list of "folders" aka labels in gmail.
    mail.select("inbox", readonly=True) # connect to inbox.
    result, data = mail.search(None, "ALL")
    id_list = data[0].split() # ids is a space separated string
    latest_email_id = id_list[-1] # get the latest
    result, data = mail.fetch(latest_email_id, encoding) # fetch the email body (RFC822) for the given ID

    return result, data

  ## Extract the core message from raw mail data
  def _extract_email(self, data):

    for response_part in data:
      if isinstance(response_part, tuple):
        return email.message_from_bytes(response_part[1])

    assert False, "Main email cannot be extracted: Wrong format!"

_client = None

def initClient(receiver, cred = [], cache = True):
  global _client
  _client = gmail(receiver, cred, cache)
  return _client

def getClient():
  global _client
  if _client == None:
    raise NameError("Client has not been initialized!")
  else:
    return _client

def initOrGetClient(receiver, cred = [], cache = True):
  global _client
  if _client == None:
    logging.warning("Client has not been explicitly initialized")
    _client = gmail(receiver, cred, cache)
    return _client
  else:
    return _client
