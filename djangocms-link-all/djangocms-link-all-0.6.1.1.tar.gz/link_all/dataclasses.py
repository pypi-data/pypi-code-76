from typing import Optional

from dataclasses import dataclass


@dataclass
class LinkAllModel:
    app_label: str
    model_name: str
    verbose_name: str = None
    url_method: Optional[str] = None
    is_show_url_in_select: bool = True
    content_type_pk: Optional[int] = None
    
    def __post_init__(self):
        self.app_label = self.app_label.lower()
        self.model_name = self.model_name.lower()
        if self.url_method is None:
            self.url_method = 'get_absolute_url'

    def __eq__(self, other: 'LinkAllModel') -> bool: 
        return (
           self.app_label == other.app_label and
           self.model_name == other.model_name
        )
