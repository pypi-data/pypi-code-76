from vizcode.constants import *
import hashlib
import vizcode.indexer as indexer
import vizcode.helpers as helpers
import vizcode.db as db
import multiprocessing
import os

NUM_PROCESSES = multiprocessing.cpu_count()

class Parsed_File:
    def __init__(self, file_path, client, write_to_db):
        self.client = client
        self.file_path = file_path
        self.write_to_db = write_to_db

# Returns a parsed file.
def parse_file(args):
    file_path, env_path, files_length, file_number = args

    if files_length is None or file_number is None:
        output = "Parsing file " + file_path
    else:
        output = str(file_number + 1) + "/" + str(files_length) + ": Parsing file " + file_path

    print(output)

    code = open(file_path, 'r').read()
    save_code_to_file(file_path, code)

    # Checks if the file path is in the cache and if the file data is not stale.
    if db.contains_file(file_path):
        data = db.get_file_data(file_path)
        if data['file'] == code and data['env_path'] == env_path:
            return Parsed_File(file_path, data['client'], False)

    client = indexer.start_indexer(file_path, code, env_path, [])

    return Parsed_File(file_path, client, True)

def save_code_to_file(file_path, code):
    """
    Saves code to a file in the frontend directory.
    """
    hashed_name = hashlib.sha256(file_path.encode('utf-8')).hexdigest()[:16]
    new_file_path = CURRENT_DIR_PATH + PUBLIC_PATH + FILE_CODE_PATH + hashed_name + ".txt"
    with open(new_file_path, 'w+') as output_file:
        output_file.write(code)

    return

def start_dir_parser(args):
    """
    start_dir_parser utilizes multiprocessing to start
    processing through all python files in a directory.
    """
    path, env_path, deselect_paths = args

    files = helpers.get_files(path, env_path, deselect_paths)
    files_length = len(files)

    print(f"Parsing {files_length} files...")
    pool = multiprocessing.Pool(NUM_PROCESSES)
    parsed_files = pool.map(parse_file, \
        [(file_path, env_path, files_length, file_number) for file_number, file_path in enumerate(files)])
    pool.close()
    pool.join()

    return parsed_files

def start_file_parser(args):
    """
    start_file_parser utilizes multiprocessing to start
    processing a python file and any python files 
    that can be reached from that file in a path of references. 
    """
    path, env_path, deselect_paths = args

    deslect_files = helpers.get_deselect_files(deselect_paths)

    if path in deslect_files:
        return []

    manager = multiprocessing.Manager()
    seen_files = set()
    seen_files.add(path)
    files = [path]

    parsed_files = manager.list()
    print(f"Parsing files...")
    while len(files) != 0:
        jobs_queue = multiprocessing.Queue()
        new_files = manager.dict()
        pool = multiprocessing.Pool(NUM_PROCESSES, worker, \
            (jobs_queue, parsed_files, new_files, env_path))

        for f in files:
            jobs_queue.put(f)

        for i in range(NUM_PROCESSES):
            jobs_queue.put(None)

        # Prevent adding anything more to the queue
        # and wait for queue to empty
        jobs_queue.close()
        jobs_queue.join_thread()

        # Prevent adding anything more to the process pool
        # and wait for all processes to finish
        pool.close()
        pool.join()

        files = []
        for f in new_files.keys():
            if f not in seen_files and f not in deslect_files:
                seen_files.add(f)
                files.append(f)

    return parsed_files

def worker(jobs_queue, parsed_files, new_files, env_path):
    """
    worker represents a process in the multiprocessing pool
    of start_file_parser.
    """
    while True:

        # Wait for items in the queue
        file_path = jobs_queue.get(block=True)
        if file_path is None:
            break

        files_length = None
        file_number = None

        parsed_file = parse_file((file_path, env_path, files_length, file_number))
        parsed_files.append(parsed_file)

        folder_path = os.path.dirname(file_path)
        refs = helpers.get_file_references(folder_path, \
            parsed_file.client.symbols)

        for ref in refs:
            new_files[ref] = None

    return 
