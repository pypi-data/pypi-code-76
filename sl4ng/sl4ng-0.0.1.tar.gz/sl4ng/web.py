from email.message import EmailMessage
import os, smtplib, subprocess

import pyperclip



def getIP(copy:bool=False) -> str:
	"""
	Returns the IP address of the device on which the function is called
	Dependencies: subprocess.check_result, pyperclip.copy
	Arguments: copy=False
	Output: ipAddress [str]
	"""
	call = str(subprocess.check_output('ipconfig')).split('\\n')
	line = [l for l in call if 'ipv4' in l.lower()][0]
	address = line.strip().strip('. ').strip('\\r').split(': ')[1]
	if copy: pyperclip.copy(address)
	return address


def quickMail(msg:str, dst:str=os.environ.get('personalEmail'), subj:str=None, head:str=None, extra:str=None, att:str=None) -> None:
	"""
	Sends a short email to the given dst using gmail's smtp configuration with default sender/receiver info taken from user environment variables
	Dependencies: os.environ.get [func], smtplib [mod], email.message.EmailMessage [obj]
	Arguments: message, **destination
	Output: None
	"""
	message = EmailMessage()
	message['Subject'] = f'{subj if subj!=None else head if head!=None else ""}'
	message['From'] = os.environ.get('promoEmail')
	message['To'] = dst
	message.set_content(msg)
	if any([subj!=None,head!=None,extra!=None]):
		message.add_alternative(f"""\
		<!DOCTYPE html>
		<html style='font-family:trebuchet ms;'>
			<body>
				<h1 style="color:SlateGray;">{head if head!=None else ''}</h1>
				<p>{msg}</p>
				<P>{extra if extra!=None else ''}
			</body>
		</html>
		""", subtype='html')
	if att != None:
		for file in att.split('*'):
			with open(file, "rb") as f:
				fileData = f.read()
				fileName = f.name.split(os.sep)[-1]
				fileType = (os.path.splitext(f.name)[1]).replace(".","")
				message.add_attachment(fileData, maintype="image", subtype=fileType, filename=fileName)
	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
		smtp.login(os.environ.get('promoEmail'), os.environ.get('promoEmailPass'))
		smtp.send_message(message)