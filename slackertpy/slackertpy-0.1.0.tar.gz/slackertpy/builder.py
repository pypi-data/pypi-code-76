from typing import Dict, List
from slackertpy import blocks


class MessageBuilder:
    def __init__(self) -> None:
        self.content = []

    def add_header(self, text: str) -> None:
        if not text:
            return

        self.content.append(blocks.Header(text).to_slack())

    def add_divider(self) -> None:
        self.content.append(blocks.Divider().to_slack())

    def add_markdown_text(self, text: str) -> None:
        if not text:
            return

        mkd_section = blocks.Section()
        mkd_section.add_field_text(text)
        self.add_section(mkd_section)

    def add_plain_text(self, text: str) -> None:
        if not text:
            return

        text_section = blocks.Section()
        text_section.add_section_text(text)
        self.add_section(text_section)

    def notify_users(self, user_ids: List[str],
                     msg_prefix: str = "Please look into this: ",
                     delim: str = " | ") -> None:
        if not user_ids:
            return

        tag_section = blocks.Section()
        user_notifs = [f"<@{user_id}>" for user_id in user_ids]
        notifs_msg = delim.join(user_notifs)
        tag_section.add_section_text(msg_prefix + notifs_msg)
        self.add_section(tag_section)

    def add_section(self, section: blocks.Section) -> None:
        self.content.append(section.to_slack())

    def prepend_section(self, section: blocks.Section) -> None:
        self.content.insert(0, section.to_slack())

    def build(self) -> Dict:
        return {
            'blocks': self.content
        }
