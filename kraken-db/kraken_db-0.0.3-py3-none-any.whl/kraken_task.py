from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2
import json
import datetime


class Task:
    def __init__(self):
        self.status = None
        self.fn_url = None
        self.task_name = None
        self.payload = None
        self.delay = None
        self.queue = None


    def post(fn_url, task_name, payload=None, delay = None, queue = 'default'):
        """ 
        Create a new google cloud task

        Provided a url and payload, schedule a task to be executed now or at a later date by puttin it in a google task queue. 

        Parameters
        ----------
        fn_url (str): The url of the function to execute
        task_name (str): The name of the task, used for deduplication
        payload (dict): The payload of the post request
        delay (int): The delay to start the task in seconds
        queue (str): The queue to use for the task (defaults to "default")

        Returns
        -------
        bool: Task success
        """

        
        # Create a client.
        client = tasks_v2.CloudTasksClient.from_service_account_json('key.json')

        # Assign config values
        project = 'kraken-v1'
        location = 'us-central1'
        in_seconds = 1


        # Construct the fully qualified queue name.
        parent = client.queue_path(project, location, queue)
        task_name = 'projects/' + project + '/locations/' + location + '/queues/' + queue + '/tasks/' + task_name


        # Build task
        if payload is not None:
            # Construct post request

            task = {
                'http_request': {  # Specify the type of request.
                    'http_method': 'POST',
                    'headers': {'Content-type': 'application/json'},
                    'url': fn_url,
                    },
                'name': task_name

                }

            # The API expects a payload of type bytes.
            #converted_payload = payload.encode()
            converted_payload = json.dumps(payload, default=str)
            converted_payload = converted_payload.encode()

            # Add the payload to the request.
            task['http_request']['body'] = converted_payload

        else:
            # Construct get request
            task = {
                'http_request': {  # Specify the type of request.
                    'http_method': 'GET',
                    'url': fn_url,
                    },
                'name': task_name

                }

        # Establish time delay
        if in_seconds is not None:
            # Convert "seconds from now" into an rfc3339 datetime string.
            d = datetime.datetime.utcnow() + datetime.timedelta(seconds=in_seconds)

            # Create Timestamp protobuf.
            timestamp = timestamp_pb2.Timestamp()
            timestamp.FromDatetime(d)

            # Add the timestamp to the tasks.
            task['schedule_time'] = timestamp


        # Send the task
        response = client.create_task(request = {'parent': parent, 'task': task})

        return response



    def get(self, task_name): 
        """ 
        Get the status o f a task

        Parameters
        ----------
        task_name (str): The name of the task

        Returns
        -------
        str: Status
        """

        a=1



    def get_all(self, queue): 
        """ 
        Get the list of active tasks in a queue
        Parameters
        ----------
        queue (str): The name of the queue

        Returns
        -------
        str: Status
        """

        a=1