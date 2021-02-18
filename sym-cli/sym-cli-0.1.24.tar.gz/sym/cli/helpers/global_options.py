from dataclasses import dataclass, field
from typing import Dict, Optional, Type

from ..data.global_options_base import GlobalOptionsBase
from ..saml_clients.chooser import choose_saml_client
from ..saml_clients.saml_client import SAMLClient


@dataclass
class GlobalOptions(GlobalOptionsBase):
    saml_client_type: Type[SAMLClient] = field(
        default_factory=lambda: choose_saml_client("auto", none_ok=True)
    )
    saml_clients: Dict[str, SAMLClient] = field(default_factory=dict)
    log_dir: Optional[str] = None
    session_length: Optional[int] = None
    aws_region: Optional[str] = None
    disable_analytics: bool = False

    def to_dict(self):
        return {
            "debug": self.debug,
            "disable_analytics": self.disable_analytics,
            "saml_client": str(self.saml_client_type),
            "session_length": str(self.session_length),
            "aws_region": str(self.aws_region),
        }
