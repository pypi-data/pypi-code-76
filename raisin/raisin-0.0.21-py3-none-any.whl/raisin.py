#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import warnings
import itertools
import time

import raisin

class Map:
    def __init__(self, target, *iterables, **kwargs):
        self.target = target
        self.iterables = iterables
        self.kwargs = kwargs
        
        self.force = kwargs["force"]
        self.timeout = kwargs["timeout"]
        self.job_timeout = kwargs["job_timeout"]
        self.save = kwargs["save"]
        self.parallelization_rate = kwargs["parallelization_rate"]
        self.ordered = kwargs["ordered"]
        self.signature = kwargs["signature"]

        self.is_started = False     # devient True quand les calculs commencent
        self.is_terminated = False  # devient True quand Run a fini
        self.die_junk = False       # devient True si il faut vite se sucider

        self.threads = []           # liste des threads (rempli par self.start())
    
    def __repr__(self):
        """
        Representation de l'objet.
        """
        return "<Map(target=%s)>" % repr(self.target)

    def _run(self):
        """
        Method representing the thread's activity.
        """
        with raisin.Printer("Recovery of results...", signature=self.signature):
            if self.parallelization_rate == 0:
                # cas ou il faut recuperer les information
                # mais que aucune parallelization n'est requieree
                for args in zip(*self.iterables):
                    if self.die_junk:
                        break
                    result = {}
                    t = time.time()
                    result["return"] = self.target(*args)
                    result["job_time"] = time.time() - t
                    if self.die_junk:
                        break
                    yield result

            elif self.parallelization_rate == 1:
                if self.ordered:
                    for thread in self.threads:
                        while thread.is_alive():
                            time.sleep(0.05)
                        if self.die_junk:
                            break
                        yield thread.get_all()
                    self.thread = []
                else:
                    while self.threads:
                        if self.die_junk:
                            break
                        for i in range(len(self.threads)):
                            if not thread.is_alive():
                                if self.die_junk:
                                    break
                                yield thread.get_all()
                                del self.threads[i]
                                break

            elif self.parallelization_rate == 2:
                raise NotImplementedError
            elif self.parallelization_rate == 3:
                raise NotImplementedError
            elif self.parallelization_rate == 4:
                raise NotImplementedError
            else:
                raise ValueError("'self.parallelization_rate' ne peut etre que 0, 1, 2, ou 4 mais pas %s" % self.parallelization_rate)
            self.is_terminated = True

    def is_alive(self):
        """
        Return whether the thread is alive.
        """
        return not self.is_terminated

    def start(self):
        """
        Start the thread's activity.
        """
        self.is_started = True
        if self.parallelization_rate == 0:
            pass
        elif self.parallelization_rate == 1:
            self.threads = [Process(
                                target=self.target,
                                args=args,
                                kwds={},
                                **self.kwargs)
                            for args in zip(*self.iterables)]
            [thread.start() for thread in self.threads]
        elif self.parallelization_rate == 2:
            raise NotImplementedError
        elif self.parallelization_rate == 3:
            raise NotImplementedError
        elif self.parallelization_rate == 4:
            raise NotImplementedError
        else:
            raise ValueError("'self.parallelization_rate' ne peut etre que 0, 1, 2, ou 4 mais pas %s." % self.parallelization_rate)

    def kill(self):
        """
        Stop imediatement tous les calculs en cours.
        """
        self.die_junk = True
        if self.parallelization_rate == 1:
            [thread.kill() for thread in self.threads]
        while self.is_alive():
            continue

    def get(self):
        """
        Cede les resultats.
        """
        if not self.is_terminated:
            if self.parallelization_rate == 0:
                yield from map(self.target, *self.iterables)
                self.is_terminated = True
            else:
                for result in self.get_all():
                    yield result["return"]

    def get_all(self):
        """
        Cede les resultats avec toutes les statistique qui vont avec
        """
        if not self.is_terminated:
            yield from self._run()

class Process:
    def __init__(self, target, args, kwds, **kwargs):
        self.target = target
        self.args = args
        self.kwds = kwds
        self.kwargs = kwargs
        self.force = kwargs["force"]
        self.timeout = kwargs["timeout"]
        self.job_timeout = kwargs["job_timeout"]
        self.save = kwargs["save"]
        self.parallelization_rate = kwargs["parallelization_rate"]
        self.signature = kwargs["signature"]

        self.is_started = False     # devient True quand les calculs commencent
        self.is_terminated = False  # devient True quand Run a fini
        self.die_junk = False       # devient True si il faut vite se sucider
    
    def __repr__(self):
        """
        Representation de l'objet
        """
        return "<Process(target=%s, args=%s, kwds=%s)>" % (repr(self.target), self.args, self.kwds)

    def _run(self):
        """
        Method representing the thread's activity.
        """
        with raisin.Printer("Recovery of the result...", signature=self.signature):
            if self.parallelization_rate == 0:
                result = {}
                t = time.time()
                result["return"] = self.target(*self.args, **self.kwds)
                result["job_time"] = time.time() - t
            elif self.parallelization_rate == 1:
                raise NotImplementedError
            elif self.parallelization_rate == 2:
                raise NotImplementedError
            elif self.parallelization_rate == 3:
                raise NotImplementedError
            elif self.parallelization_rate == 4:
                raise NotImplementedError
            self.is_terminated = True

    def is_alive(self):
        """
        Return whether the thread is alive.
        """
        return not self.is_terminated

    def start(self):
        """
        Start the thread's activity.
        """
        self.is_started = True
        if self.parallelization_rate == 0:
            pass
        elif self.parallelization_rate == 1:
            raise NotImplementedError
        elif self.parallelization_rate == 2:
            raise NotImplementedError
        elif self.parallelization_rate == 3:
            raise NotImplementedError
        elif self.parallelization_rate == 4:
            raise NotImplementedError
        else:
            raise ValueError("'self.parallelization_rate' ne peut etre que 0, 1, 2, ou 4 mais pas %s." % self.parallelization_rate)

    def kill(self):
        """
        Stop imediatement le calcul en cours.
        """
        raise NotImplementedError

    def get(self):
        """
        Retourne la valeur renvoyee par 'target(*args, **kwds)'.
        """
        if self.parallelization_rate == 0:
            return self.target(*self.args, **self.kwds)
        raise NotImplementedError

    def get_all(self):
        """
        Retourne la valeur renvoyee par 'taget(*args, **kwds)'
        et aussi les statistique qui vont autour.
        """
        raise NotImplementedError

class Scan:
    pass
