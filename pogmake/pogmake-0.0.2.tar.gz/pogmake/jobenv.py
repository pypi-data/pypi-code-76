import os
import subprocess
import logging as lg
from colorama import Fore

class JobEnv:
    """
    JobEnv class
    an 'env' object is created in each .py file's module scope. 

    And contains defaults with regards to file paths, arguments etc...
    
    It is reccomended that you use this JobEnv file in order to define/run 
    your jobs. Instead of os.system and subprocess.run(...).
    """
    def __init__(self, orig_dir, gargs):
        self.orig_dir = orig_dir 
        self.gargs = gargs
        self.verbosity_values = {
            "DEBUG" : 0,
            "INFO" : 1,
            "WARNING" : 2,
            "ERROR" : 3,
        }

    def dbg(self, ostr):
        """
        A debug print, this will only print if --verbose is passed into the program
        """
        self.log(ostr, "DEBUG")

    def log(self, ostr, verbosity=None):
        verbosity_str = verbosity
        verbo = self.verbosity_values[verbosity.upper()] if verbosity is not None else self.verbosity_values['INFO']
        set_verbo = self.verbosity_values[self.gargs.log_level]
        colors = [Fore.GREEN, "", Fore.YELLOW]

        if verbo >= set_verbo:
            print(f"{colors[verbo]}[{verbosity_str}]: {ostr}")
            
    def run(self, *run_args, cwd=None, **kwargs):
        """
        Run a job, analogous to subprocess.run, however defaults to the cwd
        that is the same as orig_dir
        """
        target_cwd = cwd
        if cwd is None:
            target_cwd = self.orig_dir
        
        subprocess.run(run_args, cwd=target_cwd)

    def system(self, systr, cwd=None):
        """
        Runs a system shell command, analogous to os.system but with a cwd
        wrapper, which will default to orig_dir
        """
        oldcwd = os.getcwd()
        
        target_cwd = cwd
        if cwd is None:
            target_cwd = self.orig_dir
            
        self.dbg(f"os.system >>> {systr} @ {cwd}")
                 
        os.chdir(target_cwd)
        os.system(systr)
        os.chdir(oldcwd)
