BLACKLISTED_FILES = {".DS_Store"}

WHITELISTED_FILEEXTS = {
    "ipynb",
}

DEFAULT_SUPPORTED_OPTIONS = {
    "frameworks": {"values": ["pytorch", "tensorflow"]},
    "machine_types": {"values": ["CPU", "K80", "V100"], "default": "CPU"},
}

VERSION_REQUIREMENTS = {"eksctl": "0.19.0", "kubectl": "1.19.0"}

# Manually update this version when eks_configure_k8s or gke_configure_k8s are modified.
# Major version updates: Update this if the user needs to recreate their cluster in order to apply the upgrade.
#     This should be avoided if at all possible. This permanently deletes all metrics and any other state the
#     user has in their cluster.
# Minor version updates: Update this for all other cases. Do not use the patch version.
SERVING_CLUSTER_VERSION = "0.14.0"
