#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
permet de gerer l'excecution des scripts
"""

import multiprocessing
import os
import threading

import raisin

__all__ = ["Orchestrator"]

def _processus(file, queue, limit_enable, permission_enable):
	process_id = os.getpid() # l'identifiant du processus pour l'os
	queue.put(process_id)	 # on communique cet identifiant au chef d'orchestre
	if file[-3:] == ".py":
		os.system("python3 " + file)
	else:
		raise ValueError("Le fichier %s n'est pas un fichier python." % repr(file))

class Orchestrator:
	"""
	Permet de gerer l'execution de plusieurs
	programes simultanemant.
	Pour chacun des programes lances, il y a un
	controle sur la ram, le cpu et les droits
	"""
	def __init__(self, signature=None):
		with raisin.Printer("Initialisation de l'orchestrateur...", signature=signature):
			self.signature = signature
			self.tasks = [] 								# c'est la liste qui contient l'ensemble des taches a effectuer
			self.ctx = multiprocessing.get_context("spawn") # cela va permetre de communiquer avec les processus enfants

	def add(self, file, *, limit_enable=False, permission_enable=False):
		"""
		ajoute le script 'file' dans la liste des taches a executer.
		
		'limit_enable' active la verifications des ressources.
		c'est a dire qu'une attention particuliere sera porte au champs:
			-limit_bandwidth
			-limit_cpu_usage
			-limit_fan_noise
			-limit_ram_usage
			qui sont present dans le fichier de configuration

		'permission_enable' active la verification de la restiction des droits.
		si le champ 'restrict_access' du fichier de configuration est a True,
		alors le script vera ces droits fortement reduit
		"""
		with raisin.Printer("Ajout du fichier %s a la file..." % repr(file), signature=self.signature):
			assert type(file) is str, "'file' doit etre un chemin vers un fichier, donc un str, pas un %s." % type(file)
			assert os.path.isfile(file), "'file' doit etre un fichier, or %s n'en est pas un!" % repr(file)
			assert len(file) >= 4 and file[-3:] == ".py", "'file' doit etre un fichier python (.py), or il ne se termine pas par '.py'."
			assert type(limit_enable) is bool, "'limit_enable' doit etre un booleen, pas un %s." % type(limit_enable)
			assert type(permission_enable) is bool, "'permission_enable' doit etre un booleen, pas un %s." % type(permission_enable)

			queue = self.ctx.Queue()
			processus = multiprocessing.Process(target=_processus, args=(file, queue, limit_enable, permission_enable))
			self.tasks.append({
				"processus": processus,
				"queue": queue,
				"file": file,
				"limit_enable": limit_enable,
				"permission_enable": permission_enable})
			return self

	def run(self):
		"""
		Lance l'execution des processus en attente
		"""
		with raisin.Printer("Lancement des %d taches..." % len(self.tasks), signature=self.signature) as p:
			for task in self.tasks:
				with raisin.Printer("Lancement de %s..." % repr(task["file"])):
					task["processus"].start()
					p.show("Restriction des ressources: %s" % task["limit_enable"])
					p.show("Restriction des droits: %s" % task["permission_enable"])
					task["process_id"] = task["queue"].get()
					p.show("Process Id: %d" % task["process_id"])


