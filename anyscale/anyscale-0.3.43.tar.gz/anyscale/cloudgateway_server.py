"""Used by the backend and CLI.
Placed in frontend/cli/anyscale package to be in the PYTHONPATH when
autoscaler searches for the module.
"""
import logging
import subprocess
import sys
from typing import Any, Dict, List
import uuid

import ray
from ray.autoscaler.node_provider import NodeProvider

from anyscale.util import send_json_request
from backend.server.services.gateway_commandrunner_service import (
    GatewaySSHCommandRunner,
)
from backend.server.services.gateway_router_service import (
    CloudGatewayException,
    CloudGatewayExceptionString,
    GatewayID,
    GatewayRequest,
)

logger = logging.getLogger(__name__)


class ServerNodeProvider(NodeProvider):  # type: ignore
    """Interface for getting and returning nodes from a Cloud gateway.

    Servers are namespaced by the `cluster_name` parameter,
    and operate on nodes within that namespace.

    Unlike standard NodeProviders, the functionality of ServerNodeProvider relies on HTTP requests
    and responses from the Cloud gateway.

    Args:
        provider_config (dict): the provider section in the cluster_config.
        cluster_name (str): the cluster name.
    """

    def __init__(
        self, provider_config: Dict[str, Any], cluster_name: str,
    ):
        self.gateway_id = str(provider_config["gateway_id"])
        self.provider_config = provider_config["subprovider"]
        self.cluster_name = cluster_name
        # TODO(ameer): uncomment this to validate user registered to this gateway
        # self._validate_registered_gateway_id(self.gateway_id)

    def _validate_registered_gateway_id(self, gateway_id: GatewayID) -> None:
        """Receives the gateway_id and checks if it is registered in the database."""
        found = False
        response = send_json_request("/api/v2/clouds/", {})
        clouds = response["results"]
        for cloud in clouds:
            if (
                cloud["provider"] == "CLOUDGATEWAY"
                and cloud["credentials"] == gateway_id
            ):
                logger.info("Loading gateway-id: " + gateway_id + " from the database.")
                found = True
                break
        if not found:
            logger.error(
                "Could not find gateway-id: "
                + self.gateway_id
                + " in the database. Did you register it?"
            )
            sys.exit()

    def get_response(self, request: GatewayRequest) -> Any:
        request["request_id"] = str(uuid.uuid4())
        request["cluster_name"] = self.cluster_name
        request["provider_config"] = self.provider_config
        ray_actor_handler = ray.get_actor("GatewayRouterActor")
        ray.get(ray_actor_handler.push_request.remote(self.gateway_id, request))
        response = ray.get(
            ray_actor_handler.pull_response.remote(
                self.gateway_id, request["request_id"]
            )
        )
        if response["data"] == CloudGatewayExceptionString:
            raise CloudGatewayException()
        return response["data"]

    def non_terminated_nodes(self, tag_filters: Dict[str, Any]) -> Any:
        request = {"type": "non_terminated_nodes", "args": (tag_filters,)}
        return self.get_response(request)

    def is_running(self, node_id: str) -> Any:
        request = {"type": "is_running", "args": (node_id,)}
        return self.get_response(request)

    def is_terminated(self, node_id: str) -> Any:
        request = {"type": "is_terminated", "args": (node_id,)}
        return self.get_response(request)

    def node_tags(self, node_id: str) -> Any:
        request = {"type": "node_tags", "args": (node_id,)}
        return self.get_response(request)

    def external_ip(self, node_id: str) -> Any:
        request = {"type": "external_ip", "args": (node_id,)}
        response = self.get_response(request)
        return response

    def internal_ip(self, node_id: str) -> Any:
        request = {"type": "internal_ip", "args": (node_id,)}
        response = self.get_response(request)
        return response

    def create_node(
        self, node_config: Dict[str, Any], tags: Dict[str, Any], count: int
    ) -> None:
        request = {
            "type": "create_node",
            "args": (node_config, tags, count),
        }
        self.get_response(request)

    def set_node_tags(self, node_id: str, tags: Dict[str, Any]) -> None:
        request = {"type": "set_node_tags", "args": (node_id, tags)}
        self.get_response(request)

    def terminate_node(self, node_id: str) -> None:
        request = {"type": "terminate_node", "args": (node_id,)}
        self.get_response(request)

    def terminate_nodes(self, node_ids: List[str]) -> None:
        request = {"type": "terminate_nodes", "args": (node_ids,)}
        self.get_response(request)

    def cleanup(self) -> None:
        request = {"type": "cleanup", "args": ()}
        self.get_response(request)

    def get_command_runner(
        self,
        log_prefix: str,
        node_id: str,
        auth_config: Dict[str, Any],
        cluster_name: str,
        process_runner: Any,
        use_internal_ip: bool,
        docker_config: Any = None,
    ) -> Any:
        """A command runner that runs on the cloud gateway."""
        cmd_runner_kwargs = {
            "log_prefix": log_prefix,
            "node_id": node_id,
            "provider": self,
            "auth_config": auth_config,
            "cluster_name": cluster_name,
            "use_internal_ip": use_internal_ip,
            "docker_config": docker_config,
        }
        # The gateway uses process_runner = subprocess.
        assert process_runner == subprocess
        return GatewaySSHCommandRunner(cmd_runner_kwargs)

    @staticmethod
    def bootstrap_config(config: Dict[str, Any]) -> Dict[str, Any]:
        """Custom bootstrap_config function to bootstrap the config through the gateway."""
        request = {"type": "bootstrap_config", "args": (config,)}
        node_provider = ServerNodeProvider(config["provider"], config["cluster_name"])
        bootstrapped_config: Dict[str, Any] = node_provider.get_response(request)
        return bootstrapped_config

    def prepare_for_head_node(self, cluster_config: Dict[str, Any]) -> Dict[str, Any]:
        # The ssh key is copied from ~/.ssh/id_rsa to ~/ray_bootstrap_key.pem using custom
        # commands in the cluster yaml.
        # After runnning these commands, ~/ray_bootstrap_key.pem becomes available on the head
        # node and we add it in the line below.
        cluster_config["auth"]["ssh_private_key"] = "~/ray_bootstrap_key.pem"
        # We also update the head node cluster config with the real provider that it should use.
        cluster_config["provider"] = cluster_config["provider"]["subprovider"]
        return cluster_config
