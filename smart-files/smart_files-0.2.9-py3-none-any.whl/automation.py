import os
import sys
from shutil import move
from pathlib import Path
import click
from crontab import CronTab

# User Variable
user = os.getenv("USER")

# Directory Variables
root_dir = f"/Users/{user}/Downloads/"
media_dir = f"/Users/{user}/Downloads/media/"
documents_dir = f"/Users/{user}/Downloads/documents/"
others_dir = f"/Users/{user}/Downloads/others/"
software_dir = f"/Users/{user}/Downloads/software/"

# Directories List
folders_to_create = [media_dir, documents_dir, others_dir, software_dir]

# Cron Vairables
python_path = sys.executable
script_path = os.path.realpath(__file__)
cron = CronTab(user=user)
command = "/usr/local/bin/smart-files run"
every_minute = f"* * * * * {command}"
hourly = f"@hourly {command}"
daily = f"@daily {command}"
weekly = f"@weekly {command}"
monthly = f"@monthly {command}"
comments_list = ["sf every minute", "sf hourly",
                 "sf daily", "sf weekly", "sf monthly"]

# category by file types
doc_types = (".doc", ".docx", ".txt", ".pdf", ".xls", ".ppt", ".xlsx", ".pptx")
media_types = (".jpg", ".jpeg", ".png", ".svg", ".gif", ".tif", ".tiff")
software_types = (".exe", ".pkg", ".dmg")


def create_dir(directories: list):
    """ Creates directories if they dont exist"""
    if type(directories) != list:
        raise TypeError("Must be a list!")
    try:
        for folder in directories:
            if not os.path.isdir(folder):
                os.mkdir(folder)
    except OSError as error:
        print(error)


def get_files(root_dir: str) -> list:
    """ Collects all non-hidden files and places them into a list """
    files = []
    for file in os.listdir(root_dir):
        if os.path.isfile(root_dir + file) and not file.startswith("."):
            files.append(file)
    return files


def move_files(files: list):
    """ Moves files to appropriate folder"""
    for file in files:
        # file moved and overwritten if already exists
        if file.endswith(doc_types):
            if os.path.isfile(documents_dir + file):
                old_file_name = file
                file = handle_dupe_files(documents_dir, file)
                os.rename(root_dir + old_file_name, root_dir + file)
            move(root_dir + file, documents_dir)
            click.secho(f"file {file} moved to {documents_dir}", fg="green")
        elif file.endswith(media_types):
            if os.path.isfile(media_dir + file):
                old_file_name = file
                file = handle_dupe_files(media_dir, file)
                os.rename(root_dir + old_file_name, root_dir + file)
            move(root_dir + file, media_dir)
            click.secho(f"file {file} moved to {media_dir}", fg="red")
        elif file.endswith(software_types):
            if os.path.isfile(software_dir + file):
                old_file_name = file
                file = handle_dupe_files(software_dir, file)
                os.rename(root_dir + old_file_name, root_dir + file)
            move(root_dir + file, software_dir)
            click.secho(f"file {file} moved to {software_dir}", fg="blue")
        else:
            if os.path.isfile(others_dir + file):
                old_file_name = file
                file = handle_dupe_files(others_dir, file)
                os.rename(root_dir + old_file_name, root_dir + file)
            move(root_dir + file, others_dir)
            click.secho(f"file {file} moved to {others_dir}", fg="magenta")


def handle_dupe_files(dir: str, file: str) -> str:
    """ Handles duplicate file names """
    count = 1
    split_array = file.split(".")
    file_extension = "." + split_array[1]
    begins_with = split_array[0]
    new_file_name = begins_with + "_" + str(count) + file_extension
    while os.path.isfile(dir + new_file_name):
        count += 1
        new_file_name = begins_with + "_" + str(count) + file_extension
    return new_file_name


def main():
    """ Runs Smart-files """
    create_dir(folders_to_create)
    files = get_files(root_dir)
    move_files(files)


def add_cron_job(frequency: str):
    """ Adds a cron job to the users crontab """
    commands = cron.find_command(command)
    exists = False
    for job in commands:
        if str(job) == frequency:
            print(f"\nCurrent Crontab Jobs:\n{cron}\n")
            click.secho(
                "\nThe cron job you requested to update already exists!\n")
            exists = True
            break
        if job.comment in comments_list:
            cron.remove(job)
            print("Your previous Smart-files cron job has been removed.")
    if not exists:
        job = cron.new(command=command)
        if frequency == every_minute:
            job.every().minute()
            job.set_comment("sf every minute")
        elif frequency == hourly:
            job.every().hour()
            job.set_comment("sf hourly")
        elif frequency == daily:
            job.every(1).dom()
            job.set_comment("sf daily")
        elif frequency == weekly:
            job.every(7).dows()
            job.set_comment("sf weekly")
        elif frequency == monthly:
            job.every(1).month()
            job.set_comment("sf monthly")

        job.enable()
        cron.write()
        click.secho("\nYour cron job has been added successfully!\n")
        return frequency


main()
