from abc import ABC, abstractmethod
from typing import Dict


class BlockElement(ABC):
    def __init__(self, element_type: str):
        self._type = element_type

    @abstractmethod
    def to_slack(self) -> Dict:
        pass


class Header(BlockElement):
    def __init__(self, text: str):
        super().__init__('header')
        self.text = text

    def to_slack(self) -> Dict:
        return {
            'type': self._type,
            'text': {
                'type': 'plain_text',
                'text': self.text
            }
        }


class Divider(BlockElement):
    def __init__(self):
        super().__init__('divider')

    def to_slack(self) -> Dict:
        return {
            'type': self._type
        }


class Section(BlockElement):
    def __init__(self):
        super().__init__('section')

        self.text = {}
        self.fields = []

    @classmethod
    def from_dict(cls, values: Dict, line_break: bool = True,
                  bold_keys: bool = True):
        section = cls()
        for key, val in values.items():
            key_text = f'*{key}*' if bold_keys else key
            key_text = key_text + '\n' if line_break else key_text
            section.add_field_text(key_text + str(val))
        return section

    def add_section_text(self, text: str, text_type: str = 'mrkdwn') -> None:
        if len(text) > 3000:
            raise ValueError("Character limit exceeded. \
                             Maximum number of characters is 3000.")
        
        self.text = {
            'type': text_type,
            'text': text
        }

    def add_field_text(self, text: str, text_type: str = 'mrkdwn') -> None:
        if len(text) > 2000:
            raise ValueError("Character limit exceeded. \
                              Maximum number of characters is 2000.")
        
        self.fields.append({
            'type': text_type,
            'text': text
        })

    def to_slack(self) -> Dict:
        section = {'type': self._type}
        if self.text:
            section['text'] = self.text
        if self.fields:
            section['fields'] = self.fields
        return section
