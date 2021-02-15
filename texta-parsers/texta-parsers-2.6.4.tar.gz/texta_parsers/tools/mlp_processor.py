import logging
import time

from . import utils
from .utils import ParserOutputType

logging.basicConfig(
    format='%(levelname)s %(asctime)s: %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S',
    level=logging.INFO
)


class MLPProcessor:

    def __init__(self, mlp, use_celery=False, app=None, worker_name="worker.taskman.mlp", queue="mlp_queue"):
        self.mlp = mlp
        self.processing_functions = {
            "Normal": self._apply_mlp,
            "Celery": self._apply_mlp_celery
        }
        self.celery = use_celery
        self.worker_name = worker_name
        self.queue = queue

        if use_celery and app:
            self.app = app

    def apply_mlp(self, generator, analyzers=["all"]):
        """ Applies MLP to objects in a given generator.
        """
        for item in generator:
            item_type = utils.get_output_type(item)

            if (item_type == ParserOutputType.EMAIL):
                email, attachments = item
                self._apply_mlp_to_mails(email, attachments, analyzers)

            elif (item_type == ParserOutputType.COLLECTION):
                self._apply_mlp_to_collection_item(item, analyzers)
            else:
                processing_function = self.processing_functions["Celery"] if self.celery else self.processing_functions[
                    "Normal"]
                cel_results = processing_function(item, 'text', analyzers)
                if self.celery:
                    for cel_result in cel_results:
                        yield cel_result

            yield item

    def _apply_mlp_celery(self, document: dict, field: str, analyzers: list):
        try:
            result = self.app.send_task(self.worker_name, queue=self.queue, args=[[document], [field], analyzers])

            while not result.ready():
                time.sleep(0.1)
                logging.info("Not Ready")

            return result.get()
        except Exception as e:
            logging.error(e)

    def _apply_mlp(self, document: dict, field: str, analyzers: list):
        if (field not in document):
            return
        content = document.get(field, "")

        if content:
            mlp_res = self.mlp.process(content, analyzers=analyzers)
            mlp_res_path = field + "_mlp"
            document[mlp_res_path] = mlp_res["text"]  # Add the MLP output dictionary.

            facts = []
            for f in mlp_res["texta_facts"]:
                f["doc_path"] = f"{mlp_res_path}.text"
                facts.append(f)

            if facts:
                document["texta_facts"] = facts

    def _apply_mlp_to_mails(self, email: dict, attachments: list, analyzers: list):
        processing_function = self.processing_functions["Celery"] if self.celery else self.processing_functions[
            "Normal"]
        processing_function(email, 'body', analyzers)
        for attachment in attachments:
            processing_function(attachment, 'content', analyzers)

    # apply it to all fields as we don't know anything about the item or it's fields
    def _apply_mlp_to_collection_item(self, item: dict, analyzers: list):
        item_copy = item.copy()
        processing_function = self.processing_functions["Celery"] if self.celery else self.processing_functions[
            "Normal"]
        for key in item_copy.keys():
            processing_function(item, key, analyzers)
