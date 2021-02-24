import base64
import copy
import json
import logging
import os
import subprocess
import threading
import time
from typing import Any, Dict

import click
from ray.autoscaler._private.providers import _get_node_provider as get_node_provider
from ray.autoscaler.node_provider import NodeProvider

from anyscale.util import send_json_request

logger = logging.getLogger(__name__)


ClusterName = str
ProviderConfig = Dict[str, Any]
ClusterConfig = Dict[str, Any]
Request = Dict[str, Any]
Response = Dict[str, Any]
# Temporary path for storing the rsynced files on the gateway node before performing
# rsync up or rsync down.
TMP_RSYNC_PATH = "/tmp/{cluster_name}/{local_path}"
# response_type could be one of five options:
# 1) RESPONSE_TYPE_FIRST_HAND_SHAKE: the dummy first message from the gateway poller
#       when the gateway starts. We check if any acknowledged cmd_runner commands
#       did not return a response. In that case we remove them from the queue.
#       We also return a new request to the main gateway thread.
# 2) RESPONSE_TYPE_HAND_SHAKE: dummy message from the gateway poller after a long timeout.
#       We also return a new request to the main gateway thread.
# 3) RESPONSE_TYPE_CMD_RUNNER_ACKNOWLEDGEMENT: an acknowledgement from the cloud gateway that it received
#       a cmd_runner request. We pop this request from the queue to avoid blocking next
#       commands from other users as cmd_runner requests might take a long time to finish.
#       We also return a new request to the main gateway thread.
# 4) RESPONSE_TYPE_CMD_RUNNER_RESPONSE: a valid cloud gateway response from a daemon thread that executed
#       a cmd_runner request (for which we previously received a RESPONSE_TYPE_CMD_RUNNER_ACKNOWLEDGEMENT response).
#       We push that response to the requester.
#       We also return an empty request, which the cloud gateway daemon thread ignores.
# 5) RESPONSE_TYPE_VALID_PROVIDER_RESPONSE: a valid cloud gateway response from executing a node provider
#       request. Since these requests are short and thus happen in serial, we pop the request
#       only after receiving its valid response, and we push that response to its requester.
#       We also return a new request to the main gateway thread.
RESPONSE_TYPE_FIRST_HAND_SHAKE = "first_handshake"
RESPONSE_TYPE_HAND_SHAKE = "handshake"
RESPONSE_TYPE_CMD_RUNNER_ACKNOWLEDGEMENT = "cmd_runner_acknowledgement"
RESPONSE_TYPE_CMD_RUNNER_RESPONSE = "valid_cmd_runner_response"
RESPONSE_TYPE_VALID_PROVIDER_RESPONSE = "valid_provider_response"


class CloudGatewayRunner:
    """Initializes and runs the cloud gateway.

    Args:
        anyscale_address (str): the address to the anyscale end point.
    """

    # Overriden in test mode to limit the number of requests to handle.
    # 1 means the cloudgateway does not stop handling requests from the server.
    # To handle two requests for example use [1,1,0].
    RUNNING = 1

    def __init__(self, anyscale_address: str) -> None:
        self.anyscale_address = anyscale_address
        self.cached_node_providers: Dict[ClusterName, NodeProvider] = {}

    def _get_bootstrapped_config(
        self, provider_config: ProviderConfig, cluster_config: ClusterConfig
    ) -> Any:
        """Receives the cluster config from the server and bootstraps it."""
        node_provider = get_node_provider(
            provider_config, cluster_config["cluster_name"]
        )
        orig_provider_config = copy.deepcopy(cluster_config["provider"])
        cluster_config["provider"] = cluster_config["provider"]["subprovider"]
        bootstrapped_config = node_provider.bootstrap_config(cluster_config)
        bootstrapped_config["provider"] = orig_provider_config
        # Cache the node provider to avoid bootstrapping for every request
        self.cached_node_providers[cluster_config["cluster_name"]] = node_provider
        return bootstrapped_config

    def _process_request(
        self,
        request: Request,
        cluster_name: ClusterName,
        provider_config: ProviderConfig,
    ) -> Response:
        """Receives the request and processes it."""
        # TODO(ameer): make it multithreaded to support simultaneous execution
        provider_request_types = [
            "non_terminated_nodes",
            "is_running",
            "is_terminated",
            "node_tags",
            "external_ip",
            "internal_ip",
            "create_node",
            "set_node_tags",
            "terminate_node",
            "terminate_nodes",
            "cleanup",
        ]
        cmd_runner_request_types = [
            "cmd_runner.run",
            "cmd_runner.run_rsync_up",
            "cmd_runner.run_rsync_down",
            "cmd_runner.remote_shell_command_str",
            "cmd_runner.run_init",
        ]
        if request["type"] == "bootstrap_config":
            cluster_config = request["args"][0]
            response = self._get_bootstrapped_config(provider_config, cluster_config)
        elif request["type"] in provider_request_types:
            if cluster_name not in self.cached_node_providers:
                self.cached_node_providers[cluster_name] = get_node_provider(
                    provider_config, cluster_name
                )
            response = self._handle_node_provider_requests(
                request, cluster_name, self.cached_node_providers[cluster_name],
            )
        elif request["type"] in cmd_runner_request_types:
            if cluster_name not in self.cached_node_providers:
                self.cached_node_providers[cluster_name] = get_node_provider(
                    provider_config, cluster_name
                )
            response = self._handle_cmd_runner_request_in_background(
                request, self.cached_node_providers[cluster_name], cluster_name
            )
        else:
            logger.error(
                "The cloud gateway does not support request of type: " + request["type"]
            )
            response = None

        if request["type"] in cmd_runner_request_types:
            # cmd_runner requests might take a long time, so we acknowledge them immediately.
            # When they finish they send a response directly to the anyscale server.
            response_message = {
                "data": response,
                "request_id": request["request_id"],
                "type": RESPONSE_TYPE_CMD_RUNNER_ACKNOWLEDGEMENT,
            }
        else:
            response_message = {
                "data": response,
                "request_id": request["request_id"],
                "type": RESPONSE_TYPE_VALID_PROVIDER_RESPONSE,
            }
        return response_message

    def _handle_cmd_runner_request_in_background(
        self, request: Request, node_provider: NodeProvider, cluster_name: ClusterName
    ) -> Any:
        """Handles command runner requests in the background.

        Immediately returns receipt acknowledgement message to the anyscale server.
        """
        thread = threading.Thread(
            target=self._handle_cmd_runner_request,
            args=(request, node_provider, cluster_name),
            daemon=True,
        )
        thread.start()
        # The response is None since the type of the message is acknowledgement.
        response = None

        return response

    def _handle_cmd_runner_request(
        self, request: Request, node_provider: NodeProvider, cluster_name: ClusterName
    ) -> Any:
        """Handles command runner requests.

        Command runner requests take a long time to finish. Therefore, this function runs in
        the background and once it finishes, it posts the response directly to the anyscale
        server.
        """
        response: Any = None
        if request["type"] == "cmd_runner.run":
            cmd_runner_kwargs, cmd, run_args, run_kwargs = request["args"]
            cmd_runner = node_provider.get_command_runner(
                **cmd_runner_kwargs, process_runner=subprocess
            )
            try:
                cmd_runner.run(cmd, *run_args, **run_kwargs)
                response = None
            except Exception as e:
                if isinstance(e, click.ClickException):
                    response = {
                        "exception_type": "click.ClickException",
                        "error_str": str(e),
                    }
                elif isinstance(e, subprocess.CalledProcessError):
                    response = {
                        "exception_type": "subprocess.CalledProcessError",
                        "returncode": e.returncode,
                        "cmd": e.cmd,
                    }
                else:
                    response = {"exception_type": "Exception", "error_str": str(e)}
        elif request["type"] == "cmd_runner.run_rsync_up":
            cmd_runner_kwargs, source, target, content, mode, options = request["args"]
            tmp_local_path = TMP_RSYNC_PATH.format(
                cluster_name=cluster_name, local_path=os.path.basename(source)
            )
            os.makedirs(
                name=TMP_RSYNC_PATH.format(cluster_name=cluster_name, local_path=""),
                exist_ok=True,
            )
            try:
                # Store file on the gateway node.
                with open(tmp_local_path, "wb") as f:
                    f.write(base64.b64decode(content))
            except PermissionError:
                logger.warning("File already exists.")
            os.chmod(tmp_local_path, mode)
            cmd_runner = node_provider.get_command_runner(
                **cmd_runner_kwargs, process_runner=subprocess
            )
            # Send file from tmp_local_path on gateway node to remote target.
            cmd_runner.run_rsync_up(tmp_local_path, target, options)
            response = None
        elif request["type"] == "cmd_runner.run_rsync_down":
            cmd_runner_kwargs, source, target, options = request["args"]
            cmd_runner = node_provider.get_command_runner(
                **cmd_runner_kwargs, process_runner=subprocess
            )
            # rsync the source file from remote node to tmp_local_path on gateway node.
            tmp_local_path = TMP_RSYNC_PATH.format(
                cluster_name=cluster_name, local_path=os.path.basename(target)
            )
            os.makedirs(
                name=TMP_RSYNC_PATH.format(cluster_name=cluster_name, local_path=""),
                exist_ok=True,
            )
            cmd_runner.run_rsync_down(source, tmp_local_path, options)
            if not os.path.isfile(tmp_local_path):
                logger.exception(
                    "The cloudgateway supports downloading a single file only."
                )
            mode = os.stat(tmp_local_path).st_mode & 0o777
            try:
                with open(tmp_local_path, "rb") as f:
                    # Decode makes it json dumpable.
                    content = base64.b64encode(f.read()).decode()
                    response = {"content": content, "mode": mode}
            except FileNotFoundError:
                response = {"content": None, "mode": None}
        elif request["type"] == "cmd_runner.remote_shell_command_str":
            cmd_runner_kwargs = request["args"]
            cmd_runner = node_provider.get_command_runner(
                **cmd_runner_kwargs, process_runner=subprocess
            )
            response = cmd_runner.remote_shell_command_str()
        elif request["type"] == "cmd_runner.run_init":
            cmd_runner_kwargs, as_head, file_mounts = request["args"]
            cmd_runner = node_provider.get_command_runner(
                **cmd_runner_kwargs, process_runner=subprocess
            )
            response = cmd_runner.run_init(as_head=as_head, file_mounts=file_mounts)
        response_message = {
            "data": response,
            "request_id": request["request_id"],
            "type": RESPONSE_TYPE_CMD_RUNNER_RESPONSE,
        }
        # Send the response directly when finished.
        send_json_request(
            self.anyscale_address,
            {"contents": json.dumps(response_message)},
            method="POST",
        )

    def _handle_node_provider_requests(
        self, request: Request, cluster_name: ClusterName, node_provider: NodeProvider,
    ) -> Any:
        """Handles node provider requests."""
        response = getattr(node_provider, request["type"])(*request["args"])
        return response

    def gateway_run_forever(self) -> None:
        """Long polls anyscale server."""

        response_message: Dict[str, Any] = {
            "data": "dummy_message",
            "request_id": "0",
            "type": RESPONSE_TYPE_FIRST_HAND_SHAKE,
        }
        while self.RUNNING:
            try:
                request = send_json_request(
                    self.anyscale_address,
                    {"contents": json.dumps(response_message)},
                    method="POST",
                )
            except Exception:
                logger.exception("Could not connect to Anyscale server. Retrying...")
                response_message = {
                    "data": "dummy_message",
                    "request_id": "0",
                    "type": RESPONSE_TYPE_HAND_SHAKE,
                }
                time.sleep(10)
                continue
            logger.info("Received request: " + str(request["result"]["type"]))
            try:
                response_message = self._process_request(
                    request["result"],
                    request["result"]["cluster_name"],
                    request["result"]["provider_config"],
                )
            except Exception as e:
                # Gateway Error.
                logger.exception(type(e).__name__ + ": " + str(e))
                response_message = {
                    "data": type(e).__name__ + ": " + str(e),
                    "request_id": request["result"]["request_id"],
                    "type": RESPONSE_TYPE_VALID_PROVIDER_RESPONSE,
                }
