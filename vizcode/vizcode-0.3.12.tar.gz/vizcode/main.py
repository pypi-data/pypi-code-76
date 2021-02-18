from vizcode.graph import Graph
from vizcode.command_line import Command_Line
from vizcode.constants import *
import vizcode.parsing as parsing
import vizcode.helpers as helpers
import vizcode.db as db
import os

def main(parsed_files):

    graph = Graph("Newspark Python Example")

    graph.populate_graph(parsed_files)
    print("\nBuilt the graph.")

    graph.save_graph()
    print("Saved the graph.")

    print("Starting frontend application...\n")
    graph.start_frontend()

    return None

def start():

    args = Command_Line()

    # Parse the arguments from the Command Line
    path = args.get_path()
    env_path = args.get_env()
    deselect_paths = args.get_deselect()

    # Checks to make sure the paths for the source code,
    # environment, test path are valid
    exists = True
    if not os.path.exists(path):
        print ("Path does not exist.")
        exists = False

    if exists:
        if env_path and not os.path.exists(env_path):
            print ("Not a valid environment path, \
                will default to global environment")
            env_path = None
        
        valid_deselect_paths = []
        for subpath in deselect_paths:
            if not os.path.exists(subpath) and not os.path.isfile(subpath):
                print (subpath + ": invalid object to deselect for visualization, will remove")
            else:
                valid_deselect_paths.append(subpath)

        helpers.remove_old_code()

        entered_info = False
        creds = None
        if not os.path.exists(CURRENT_DIR_PATH + CREDENTIALS_PATH):
            print("We see this is your first time using VizCode. " + \
            "Please fill out some basic info below to get started.")
            creds = helpers.write_credentials()
            entered_info = True

        while not helpers.valid_credentials():
            creds = helpers.write_credentials()
            entered_info = True
        
        if entered_info:
            print(f"\nThanks for entering your info {creds['name']}! " + \
                "VizCode will start parsing your code shortly.\n")
        else:
            helpers.update_credentials()

        parsed_files = None
        if os.path.isdir(path):
            parsed_files = parsing.start_dir_parser((path, env_path, valid_deselect_paths))

        elif '.py' in path:
            parsed_files = parsing.start_file_parser((path, env_path, valid_deselect_paths))

        # Writes parsed files to the db if they have a true write_to_db tag. 
        for parsed_file in parsed_files:
            if parsed_file.write_to_db:
                db.store_parsed_file(parsed_file, env_path)

        if parsed_files:
            main(parsed_files)