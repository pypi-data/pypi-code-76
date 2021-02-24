import os
import time
import glob
from pathlib import Path
import re
import logging
import importlib
import importlib.util
import traceback
from fk.batch.db import Database
import fk.utils
import fk.utils.Watchdog
from pprint import pformat


logger = logging.getLogger(__name__)


class BatchProcessor:
    def __init__(self, config):
        self.config = config
        # How many ids to batch simultaneously
        # self.batch_size=self.config.get('batch-log-batch-size', 10)
        # self.item_types=['scrape']
        # self.item_queues={}
        # for type in self.item_types:
        # 	self.item_queues[type]=Queue(self.batch_size)
        # Lock to synchronize access to our source of new ids to try
        # self.id_source_lock=threading.Lock()
        # How many simultaneous threads will be processing batch items?
        # self.thread_count=1
        self.task_filter = re.compile("^([0-9a-z\-_]+)$")
        self.last_status_time = None
        self.callables = {}
        self.entry_name = "batch_filter_entrypoint"
        if self.config.get("db-hostname", "skip") == "skip":
            logger.warning("Skipping database initialization")
        else:
            self.db = Database(self.config)

    def verify(self):
        modules = self.list_modules()
        ok = []
        failed = []
        for (name, error) in modules:
            if error:
                failed.append((name, error))
            else:
                ok.append(name)
        if ok:
            logger.info("Available modules:")
            for name in ok:
                logger.info(f" + '{name}'")
        if failed:
            message = ""
            logger.info("Failed modules:")
            for (name, error) in failed:
                logger.error(f" + '{name}': {error}")
                message += f"{name}: {error}\n"
            return False, message
        return True, ""

    def load_module_by_filepath(self, module_name, module_filepath):
        module = None
        failure = None
        try:
            spec = importlib.util.spec_from_file_location(module_name, module_filepath)
            spec.submodule_search_locations = list(__import__(__name__).__path__)
            module = importlib.util.module_from_spec(spec)
            # logger.info(f"ORIG MODULE PATH: {pformat(module.__path__)}")
            # logger.info(f"PARENT PATH: {pformat(__import__(__name__).__path__)}")
            # module.__path__= __import__(__name__).__path__
            # logger.info(f"UPDATED MODULE PATH: {pformat(module.__path__)}")
            # sys.modules[spec.name] = module
            spec.loader.exec_module(module)
        except Exception as e:
            failure = f"Import of module '{module_name}'from file '{module_filepath}' had errors ({e})"
            module = None
        return module, failure

    def load_module_by_package(self, module_name, package_path=None):
        module = None
        failure = None
        try:
            module = importlib.import_module(module_name, package_path)
        except Exception as e:
            failure = f"Import of module '{module_name}'from package '{package_path}' had errors ({e})"
            module = None
        return module, failure

    def get_item_types(self):
        module_root_raw = self.config.get("batch-filter-root", "/tmp/inexistant")
        module_root_object = Path(module_root_raw).resolve(strict=False)
        module_root = module_root_object.as_posix()
        if not module_root:
            logger.warning("Module root was not set")
        if not os.path.exists(module_root):
            logger.warning(f"Module root '{module_root}' did not exist")
        logger.info(f"Looking for types in '{module_root}':")
        ret = {}
        for path_object in module_root_object.rglob("*.py"):
            path_object = path_object.resolve(strict=False)
            path = path_object.as_posix()
            if path_object.name.startswith("__"):
                logger.warning(f"Skipping invalid path {path}")
                continue
            if not path.startswith(module_root):
                logger.warning(f"Skipping invalid path {path}")
                continue
            path_difference = path[len(module_root) + 1 :]
            name = Path(path_difference).with_suffix("").as_posix()
            ret[name] = path
            logger.info(f"  Found {name} (from {path})")
        return ret

    def list_modules(self):
        module_root_raw = self.config.get("batch-filter-root", "/tmp/inexistant")
        module_root_object = Path(module_root_raw).resolve(strict=False)
        module_root = module_root_object.as_posix()

        ret = []
        failure = None
        if not module_root:
            ret.append(("module_root", f"Module root was not set"))
        elif not os.path.exists(module_root):
            ret.append(("module_root", f"Module root '{module_root}' did not exist"))
        else:
            files_objects = module_root_object.rglob("*.py")
            for file_object in files_objects:
                module_filepath = file_object.as_posix()
                if not module_filepath:
                    logger.warn(f"Not posix path: {file_object}")
                    continue
                if file_object.name.startswith("__"):
                    logger.warn(f"Skipping internal: {file_object}")
                    continue
                if fk.utils.file_contains_str(module_filepath, self.entry_name):
                    try:
                        module, failure = self.load_module_by_filepath(module_filepath, module_filepath)
                        if module:
                            if hasattr(module, self.entry_name):
                                entry_method = getattr(module, self.entry_name)
                                if not callable(entry_method):
                                    entry_method = None
                                    failure = f"Entrypoint was not callable in filter module {module_filepath}"
                            else:
                                failure = f"Filter module {module_filepath} did not have method {self.entry_name}"
                        else:
                            failure = f"Filter module {module_filepath} could not be loaded because: {failure}"
                    except Exception as e:
                        failure = f"Import of module '{module_filepath}' had errors and was skipped ({e})"
                else:
                    failure = f"No entrypoint found in filter module {module_filepath}"
                # logger.warn(f"Appending stat: {module_filepath}:{failure}")
                ret.append((module_filepath, failure))
        return ret

    def get_callable_for_type_raw(self, type):
        match = self.task_filter.match(type)
        module_name = None
        entry_method = None
        failure = None
        # Is this a match?
        if match:
            # Exctract the data we want
            module_name = match.group(1)
            module_filename = module_name + ".py"
            module_filepath = os.path.join(self.config.get("batch-filter-root", "/dev/null"), module_filename)
            module = None
            if os.path.exists(module_filepath):
                if fk.utils.file_contains_str(module_filepath, self.entry_name):
                    try:
                        # module = importlib.import_module(module_name)
                        module, failure = self.load_module_by_filepath(module_name, module_filepath)
                        # module, failure = self.load_module_by_package('fk.batch.filters.'+module_name)
                        if module:
                            if hasattr(module, self.entry_name):
                                entry_method = getattr(module, self.entry_name)
                                if not callable(entry_method):
                                    entry_method = None
                                    failure = f"Entrypoint was not callable in filter module {module_filepath}"
                            else:
                                failure = f"Filter module {module_filepath} did not have method {self.entry_name}"
                        else:
                            failure = f"Filter module {module_filepath} could not be loaded because: {failure}"
                    except Exception as e:
                        failure = f"Import of module '{module_name}' had errors and was skipped ({e})"
                else:
                    failure = f"No entrypoint found in filter module {module_filepath}"
            else:
                failure = f"Could not find filter module {module_filepath}"
        return entry_method, failure

    def get_callable_for_type(self, type):
        if type in self.callables:
            return self.callables.get(type)
        else:
            callable = self.get_callable_for_type_raw(type)
            if callable:
                self.callables[type] = callable
            return callable

    def _execute_safely(self, entrypoint, item):
        # logger.info("SAFE EXECUTION STARTED!")
        # We cap runtime at 60 seconds
        timeout = 30
        failure = None
        result = None
        try:
            watchdog = fk.utils.Watchdog.Watchdog(timeout)
            # logger.info("££££ Entry")
            result, failure = entrypoint(item, self.config)
            # logger.info("££££ Exit")
        except fk.utils.Watchdog.Watchdog:
            logger.warning("Watchdag triggered exception")
            failure = f"execution timed out after {timeout} seconds"
        except Exception as e:
            logger.warning("")
            logger.warning("")
            logger.warning(f"###############################################")
            logger.warning(f"#    Batch item: {item}")
            logger.warning(f"# Failed with: {e}")
            failure = f"{e}"
            logger.warning(f"#          At:")
            traceback.print_exc()
            logger.warning(f"#######################################")
            logger.warning("")
            logger.warning("")
        watchdog.stop()
        # logger.info("SAFE EXECUTION FINISHED!")
        return result, failure

    def execute_one_batch_item(self):
        """
        Take ownership of one batch item and make sure it is properly executed and updated with status underway
        """
        item = self.db.book_batch_item(self.db.PENDING, self.db.IN_PROGRESS)
        if item:
            # logger.info("Processing item:")
            # logger.info(pformat(item))
            id = item.get("id", None)
            type = item.get("type", None)
            updated_at = item.get("updated_at", None)
            if id and type and updated_at:
                entrypoint, failure = self.get_callable_for_type(type)
                if entrypoint and failure:
                    entrypoint = None
                    failure = f"{failure} AND ENTRYPOINT WAS SET!"
                result = None
                if entrypoint:
                    result, failure = self._execute_safely(entrypoint, item)
                if failure:
                    logger.warning("¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤ BATCH FILTER FAILED WITH ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤")
                    logger.warning(failure)
                    logger.warning("")
                id2, updated_at2 = self.db.bump_batch_item(id=id, status=self.db.FAILED if failure else self.db.DONE, error=failure, updated_at=updated_at, result=result) or (None, None)
                # logger.info(f"id2={id2}, updated_at2={updated_at2}, id={id}, updated_at={updated_at}")
            else:
                logger.warning(f"Missing data for item id={id}, type={type}, updated_at={updated_at}")

        # else:
        # logger.info(f"No pending items found")

    def insert_batch_item(self, type="test", data=None, result=None, priority=50, source=None):
        """
        Insert a new batch item into the database, ready for execution
        """
        # fmt: off
        return self.db.insert_batch_item(
            {
                "priority": priority,
                "data": data,
                "result": result,
                "type": type,
                "status": self.db.PENDING,
                "source": source
            }
        )
        # fmt: on

    def retry_hung_jobs_older_than(self, time_sec=30):
        self.db.bump_batch_items(self.db.IN_PROGRESS, self.db.PENDING, time_sec)

    def delete_hung_jobs_older_than(self, time_sec=30):
        self.db.delete_batch_items_with_status_older_than(self.db.IN_PROGRESS, time_sec)

    def delete_failed_jobs(self):
        self.db.delete_batch_items_with_status_older_than(self.db.FAILED, 0)

    def delete_all_jobs(self, time_sec=30):
        self.db.delete_all()

    def get_status(self):
        status = {"type": self.db.get_type_counts(), "status": self.db.get_status_counts(), "last": self.db.get_last_jobs(limit=10), "type_status": self.db.get_type_status_counts()}
        return status

    def process(self):
        if not self.execute_one_batch_item():
            # Put a status
            # if not self.last_status_time or (datetime.now() - self.last_status_time).total_seconds() > 10.0:
            # 	self.print_status()
            # Lets not get stuck in a loop!
            time.sleep(1)
