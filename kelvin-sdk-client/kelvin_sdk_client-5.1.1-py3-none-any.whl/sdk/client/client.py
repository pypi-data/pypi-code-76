"""
Kelvin API Client.
"""

from __future__ import annotations

from functools import wraps
from types import FunctionType, MethodType
from typing import Any, Generic, List, Mapping, Type, TypeVar

from .base_client import BaseClient
from .data_model import DataModel
from .model import responses

MODELS: Mapping[str, Type[DataModel]] = {
    "acp": responses.ACP,  # type: ignore
    "acp_edge_app_version": responses.ACPEdgeAppVersion,  # type: ignore
    "acp_meta_data_item": responses.ACPMetaDataItem,  # type: ignore
    "acp_metadata": responses.ACPMetadata,  # type: ignore
    "acp_metrics": responses.ACPMetrics,  # type: ignore
    "acp_status": responses.ACPStatus,  # type: ignore
    "app": responses.App,  # type: ignore
    "app_version": responses.AppVersion,  # type: ignore
    "app_version_status": responses.AppVersionStatus,  # type: ignore
    "audit_logger": responses.AuditLogger,  # type: ignore
    "cluster": responses.Cluster,  # type: ignore
    "cluster_cidr_item": responses.ClusterCIDRItem,  # type: ignore
    "cluster_manifest_list": responses.ClusterManifestList,  # type: ignore
    "data_label": responses.DataLabel,  # type: ignore
    "data_label_cluster": responses.DataLabelCluster,  # type: ignore
    "data_model": responses.DataModel,  # type: ignore
    "data_model_schema": responses.DataModelSchema,  # type: ignore
    "instance_health_status": responses.InstanceHealthStatus,  # type: ignore
    "instance_settings": responses.InstanceSettings,  # type: ignore
    "label": responses.Label,  # type: ignore
    "label_metadata": responses.LabelMetadata,  # type: ignore
    "orchestration_provision": responses.OrchestrationProvision,  # type: ignore
    "secret": responses.Secret,  # type: ignore
    "storage": responses.Storage,  # type: ignore
    "user": responses.User,  # type: ignore
    "user_with_permissions": responses.UserWithPermissions,  # type: ignore
    "view": responses.View,  # type: ignore
    "view_group": responses.ViewGroup,  # type: ignore
    "view_group_metadata": responses.ViewGroupMetadata,  # type: ignore
    "view_item": responses.ViewItem,  # type: ignore
    "view_metadata": responses.ViewMetadata,  # type: ignore
    "view_type": responses.ViewType,  # type: ignore
    "view_type_metadata": responses.ViewTypeMetadata,  # type: ignore
    "wireguard_peer": responses.WireguardPeer,  # type: ignore
    "wireguard_tunnel": responses.WireguardTunnel,  # type: ignore
    "workload": responses.Workload,  # type: ignore
    "workload_logs": responses.WorkloadLogs,  # type: ignore
    "workload_metrics": responses.WorkloadMetrics,  # type: ignore
    "workload_status_item": responses.WorkloadStatusItem,  # type: ignore
}


T = TypeVar("T", bound=DataModel)


class DataModelProxy(Generic[T]):
    """Proxy client to data models."""

    def __init__(self, model: Type[T], client: Client) -> None:
        """Initialise resource adaptor."""

        self._model = model
        self._client = client

    def new(self, **kwargs: Any) -> T:
        """New instance."""

        return self._model(self._client, **kwargs)

    def __getattr__(self, name: str) -> Any:
        """Map name to method."""

        if name.startswith("_"):
            return super().__getattribute__(name)

        try:
            f = getattr(self._model, name)
        except AttributeError:
            return super().__getattribute__(name)

        if isinstance(f, (FunctionType, MethodType)):

            @wraps(f)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                return f(*args, **kwargs, client=self._client)

            return wrapper

        return super().__getattribute__(name)

    def __dir__(self) -> List[str]:
        """List methods for model."""

        return sorted(
            k
            for k in vars(self._model)
            if not k.startswith("_")
            and isinstance(getattr(self._model, k), (FunctionType, MethodType))
        )

    def __str__(self) -> str:
        """Return str(self)."""

        return str(self._model)

    def __repr__(self) -> str:
        """Return repr(self)."""

        return repr(self._model)


class Client(BaseClient):
    """
    Kelvin API Client.

    Parameters
    ----------
    config : :obj:`ClientConfiguration`, optional
        Configuration object
    password : :obj:`str`, optional
        Password for obtaining access token
    totp : :obj:`str`, optional
        Time-based one-time password
    verbose : :obj:`bool`, optional
        Log requests/responses
    use_keychain : :obj:`bool`, optional
        Store credentials securely in system keychain
    store_token : :obj:`bool`, optional
        Store access token
    login : :obj:`bool`, optional
        Login to API
    mirror : :obj:`str`, optional
        Directory to use for caching mirrored responses (created if not existing)
    mirror_mode : :obj:`MirrorMode`, :obj:`str` or :obj:`list`, optional
        Mode of response mirroring:
            - ``dump``: Save responses in mirror cache
            - ``load``: Load responses from mirror cache (if available)
            - ``both``: Both dump and load
            - ``none``: Do not dump or load
    _adapter : :obj:`requests.adapters.BaseAdapter`, optional
        Optional requests adapter instance (e.g. :obj:`requests.adapters.HTTPAdapter`).
        Useful for testing.

    """

    acp: Type[responses.ACP]
    acp_edge_app_version: Type[responses.ACPEdgeAppVersion]
    acp_meta_data_item: Type[responses.ACPMetaDataItem]
    acp_metadata: Type[responses.ACPMetadata]
    acp_metrics: Type[responses.ACPMetrics]
    acp_status: Type[responses.ACPStatus]
    app: Type[responses.App]
    app_version: Type[responses.AppVersion]
    app_version_status: Type[responses.AppVersionStatus]
    audit_logger: Type[responses.AuditLogger]
    cluster: Type[responses.Cluster]
    cluster_cidr_item: Type[responses.ClusterCIDRItem]
    cluster_manifest_list: Type[responses.ClusterManifestList]
    data_label: Type[responses.DataLabel]
    data_label_cluster: Type[responses.DataLabelCluster]
    data_model: Type[responses.DataModel]
    data_model_schema: Type[responses.DataModelSchema]
    instance_health_status: Type[responses.InstanceHealthStatus]
    instance_settings: Type[responses.InstanceSettings]
    label: Type[responses.Label]
    label_metadata: Type[responses.LabelMetadata]
    orchestration_provision: Type[responses.OrchestrationProvision]
    secret: Type[responses.Secret]
    storage: Type[responses.Storage]
    user: Type[responses.User]
    user_with_permissions: Type[responses.UserWithPermissions]
    view: Type[responses.View]
    view_group: Type[responses.ViewGroup]
    view_group_metadata: Type[responses.ViewGroupMetadata]
    view_item: Type[responses.ViewItem]
    view_metadata: Type[responses.ViewMetadata]
    view_type: Type[responses.ViewType]
    view_type_metadata: Type[responses.ViewTypeMetadata]
    wireguard_peer: Type[responses.WireguardPeer]
    wireguard_tunnel: Type[responses.WireguardTunnel]
    workload: Type[responses.Workload]
    workload_logs: Type[responses.WorkloadLogs]
    workload_metrics: Type[responses.WorkloadMetrics]
    workload_status_item: Type[responses.WorkloadStatusItem]

    def __dir__(self) -> List[str]:
        """Return list of names of the object items/attributes."""

        return [*super().__dir__(), *MODELS]

    def __getattr__(self, name: str) -> Any:
        """Get attribute."""

        if name.startswith("_") or name in super().__dir__():
            return super().__getattribute__(name)  # pragma: no cover

        try:
            model = MODELS[name]
        except KeyError:
            return super().__getattribute__(name)

        return DataModelProxy(model, self)
