# -*- coding: utf-8 -*-
"""HostHome-CLI ara login y empezara tu cli
Usage:
    hosthome          [-h | --help]
    hosthome empezar  [--verbose]
    hosthome eliminar [--verbose]
    hosthome info id
    hosthome          [-v | --version]

Argumentos:
    --help -h          :: Enseña este mensage
    --verbose          :: Dice lo que esta pasando
    --version -v       :: Da la version del CLI
"""

from docopt import docopt
import platform
from termcolor import cprint
from warnings import warn
import sys, os, requests

from hosthome.version import VERSION as __version__
from hosthome.login import login

import inquirer

url = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()["url"]
docs = requests.get("https://raw.githubusercontent.com/HostHome-of/config/main/config.json").json()["docs"]   

archivo = """
run = "tempCmdStart"
len = "tempLen"

----- ADVERTENCIA
NO MENTIR SOBRE LA INFORMACION SINO EL HOST SERA ELIMINADO
NO TOCAR NADA A NO SER QUE SEA NECESARIO

SI OCURRE UN ERROR PODEIS PONERLO AQUI (https://github.com/HostHome-oficial/python-CLI/issues)
-----
"""

def crearArchivo(Lenguage: str, cmd: str, verbose: bool):
  if verbose:
    print("\n ---- Logs")
    print("Creando archivo...")
  try:
    data = open(".hosthome", "x")
  except:
    if verbose:
      print("Archivo localizado")
      print("Eliminando archivo...")
    os.remove(".hosthome")
    if verbose:
      print("Recreando...")
    data = open(".hosthome", "x")
  if verbose:
    print("Escribiendo archivo...")
  archivo2 = str(archivo
                .replace("tempLen", Lenguage)
                .replace("tempCmdStart", cmd)
                )
  data.write(archivo2)
  cprint("¡ya esta!", "green")

def main():
  """HostHome-CLI ara login y empezara tu cli
  Usage:
      hosthome          [-h | --help]
      hosthome empezar  [--verbose]
      hosthome eliminar [--verbose]
      hosthome info id
      hosthome          [-v | --version]

  Argumentos:
      --help -h          :: Enseña este mensage
      --verbose          :: Dice lo que esta pasando
      --version -v       :: Da la version del CLI
  """

  try:
    args = docopt(__doc__, version="HostHome-CLI | pip :: v = {}".format(__version__))

    if platform.system() != "Windows":
      warn("Encontré un sistema que no es Windows. Es posible que algo no funcione.")

    if args["empezar"]:    
      verbose = False
      data = login()
      cprint(f"\nBienvenido {data['nombre']}\n", "green")

      questions = [
        inquirer.Text('cmd', message="Pon el comando de ejecucion"),
        inquirer.List('len',
                      message="Cual es tu lenguage de programacion?",
                      choices=["ruby", "python", "nodejs", "scala", "clojure", "cs", "php"],
                  )
      ]

      answers = inquirer.prompt(questions)

      instalacion = answers["cmd"]
      lenguage = answers["len"]

      if args["--verbose"]:
        verbose = True

      crearArchivo(lenguage, instalacion, verbose)

      sys.exit(0)

    print(
  """HostHome-CLI ara login y empezara tu cli
  Uso:
      hosthome          [-h | --help]
      hosthome empezar  [--verbose]
      hosthome eliminar [--verbose]
      hosthome info id
      hosthome          [-v | --version]

  Argumentos:
      --help -h          :: Enseña este mensage
      --verbose          :: Dice lo que esta pasando
      --version -v       :: Da la version del CLI
  """
    )
  except Exception as e:
    print(e)