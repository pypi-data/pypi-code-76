# -*- coding: utf-8 -*-

from urllib.request import urlretrieve
import importlib
import os
import pathlib
import shutil
from distutils.dir_util import copy_tree
from datetime import datetime
import time

from orbis_eval.config import paths
from orbis_eval.libs.decorators import clear_screen
from orbis_eval.libs.config import load_config

import tkinter as tk
from tkinter import filedialog

import logging
logger = logging.getLogger(__name__)


class Main(object):
    """docstring for Main"""

    def __init__(self, addon_path):
        super(Main, self).__init__()
        self.addon_path = addon_path
        self.config = load_config([f"{self.addon_path}/sources.yaml"])[0]
        self.available_corpora = {}
        self.choice = {}
        self.selection = None
        self.local = False

    def select_location(self):
        print("Please select the location of the corpus:")
        print(f'[1]:\t Load local corpus file')
        print(f'[2]:\t Load file from gerbil')
        choice = int(input("Selection: "))
        if choice == 1:
            self.local = True

    def fetch_available(self):
        for file_format in self.config['corpora']:
            for source in self.config['corpora'][file_format]:
                module_path = f"orbis_addon_repoman.corpora.{source}.main"
                imported_module = importlib.import_module(module_path)
                corpora = imported_module.list_available_corpora(self.config)
                self.available_corpora[source] = corpora

    @clear_screen()
    def select(self):
        """
        hacking it to work... dont judge me. will fix
        """
        print(self.local)
        if self.local:
            self.choice[0] = ["local", None, None, "local"]
            self.selection = 0
        else:
            print("anyway")
            self.fetch_available()
            print("Please select the corpus you want to download:")

            counter = 0
            for source, item in self.available_corpora.items():
                source_hash = len(source) * "#"
                print(f"\n{source}\n{source_hash}")

                for corpus in self.available_corpora[source]:
                    print(f'[{counter}]:\t {corpus[0]} ({corpus[2]})')
                    self.choice[counter] = *corpus, source
                    counter += 1

            self.choice[counter] = ["local", None, None, "local"]

            self.selection = int(input("Selection: "))

    def down_and_load(self):

        action = "load" if self.choice[self.selection][0] == "local" else "download"

        if action == "load":
            file_destination, corpus_dir, file_name, corpus_url, download_time = self.load()
        else:
            file_destination, corpus_dir, file_name, corpus_url, download_time = self.download()

        if not self.choice[self.selection][2]:
            file_ending = file_name.split(".")[-1]
            print(f"71: {file_name} File ending: {file_ending}")

            module_name = None
            is_nif = input("Is this a NIF file? (Y/n)")
            if is_nif in ["Y", "y", ""]:
                module_name = "nif"
            else:
                is_wl_harvest = input("Should json files be loaded? (Y/n)")
                if is_wl_harvest in ["Y", "y", ""]:
                    module_name = "json"
                else:
                    file_destination = None
        else:
            module_name = self.choice[self.selection][2]

        if file_destination:
            module_path = f"orbis_addon_repoman.format.{module_name}.main"
            imported_module = importlib.import_module(module_path)
            imported_module.run(file_destination, corpus_dir, file_name, corpus_url, download_time)
        else:
            print("No file available.")
            time.sleep(5)
            self.select()

    def source_exists(self, corpus_dir):
        if pathlib.Path(corpus_dir).is_dir():
            print(f"Corpus might exist already. A folder with the same name has been found: {corpus_dir}")
            overwrite = input("Do you want to overwrite it? (Y/n) ")
            if overwrite not in ["Y", "y", ""]:
                print("Download canceled.")
                return True
        return False

    def download(self):

        corpus_url = self.choice[self.selection][1]
        download_name = corpus_url.split("/")[-1].split(".")[0]
        corpus_dir = os.path.join(paths.corpora_dir, download_name.lower())

        if not self.source_exists(corpus_dir):
            pathlib.Path(corpus_dir).mkdir(parents=True, exist_ok=True)
            download_name = corpus_url.split("/")[-1].split(".")[0]
            download_filetype = corpus_url.split("/")[-1].split(".")[-1]
            download_destination = os.path.join(corpus_dir, "source")
            pathlib.Path(download_destination).mkdir(parents=True, exist_ok=True)
            download_destination = os.path.join(download_destination, f"{download_name}.{download_filetype}")
            print(f"Downloading {corpus_url}", end="\r")
            urlretrieve(corpus_url, download_destination)
            print(f"Downloading {corpus_url} finished")
            download_time = datetime.now()

            return download_destination, corpus_dir, download_name, corpus_url, download_time
        return False

    def ask_for_format(self):
        module_path = f"orbis_addon_repoman.format"
        format_list = os.listdir(module_path)
        print("What's the format of the corpus?")

        for idx, format_name in enumerate(format_list):
            space = 5 - len(str(idx))
            print(f"[{idx}]{space * ' '}{format_name}")

        selected_format = int(input("\nPlease select format: "))

        return format_list[selected_format]

    def load(self):

        print("What do you want to open?")
        print("[1] file")
        print("[2] folder containing json files")

        selection = input("Please select: ")
        root = tk.Tk()
        root.withdraw()

        if selection == "1":
            file_path = filedialog.askopenfilename(
                initialdir=pathlib.Path.home(),
                title="Select file",
                filetypes=(
                    ("ttl files", "*.ttl"),
                    ("json files", "*.json"),
                    ("all files", "*.*")
                )
            )

            file_name = ".".join(file_path.split("/")[-1].split(".")[:-1])

            print(f"file_name: {file_name}")
            file_name_ok = input(f'Is the corpus called "{file_name}"? (Y/n) ')
            while file_name_ok not in ["Y", "y", ""]:
                file_name = input("Please enter corpus name: ")
                file_name_ok = input(f"Is the corpus name {file_name} ok? (Y/n) ")

            corpus_dir = os.path.join(paths.corpora_dir, file_name.lower())
            if not self.source_exists(corpus_dir):

                pathlib.Path(corpus_dir).mkdir(parents=True, exist_ok=True)
                file_filetype = file_path.split("/")[-1].split(".")[-1]

                file_destination = os.path.join(corpus_dir, "source")
                pathlib.Path(file_destination).mkdir(parents=True, exist_ok=True)
                file_destination = os.path.join(file_destination, f"{file_name}.{file_filetype}")
                print(f"file_path: {file_path}")
                print(f"file_destination: {file_destination}")

                shutil.copy(str(file_path), str(file_destination))
                download_time = datetime.now()
                return file_destination, corpus_dir, file_name, "local_file", download_time

        elif selection == "2":
            file_path = filedialog.askdirectory(
                initialdir=pathlib.Path.home() / "ownCloud" / "Projects" / "Orbis" / "src",
                title="Select folder"
            )

            print(file_path)
            file_name = file_path.split("/")[-1]

            print(f"file_name: {file_name}")
            file_name_ok = input(f'Is the corpus called "{file_name}"? (Y/n) ')
            while file_name_ok not in ["Y", "y", ""]:
                file_name = input("Please enter corpus name: ")
                file_name_ok = input(f"Is the corpus name {file_name} ok? (Y/n) ")

            corpus_dir = os.path.join(paths.corpora_dir, file_name.lower())

            if not self.source_exists(corpus_dir):

                pathlib.Path(corpus_dir).mkdir(parents=True, exist_ok=True)

                file_destination = os.path.join(corpus_dir, "source")

                print(f"file_path: {file_path}")
                print(f"file_destination: {file_destination}")

                dirpath = pathlib.Path(file_destination)
                if dirpath.exists() and dirpath.is_dir():
                    shutil.rmtree(dirpath)
                    dirpath.mkdir(parents=True, exist_ok=True)

                copy_tree(str(file_path), str(file_destination))
                download_time = datetime.now()

                return file_destination, corpus_dir, file_name, "local_file", download_time
        else:
            print("Invalid selection. Please try again!")
            self.load()

        return False

    def run(self):
        self.select_location()
        self.select()
        self.down_and_load()
