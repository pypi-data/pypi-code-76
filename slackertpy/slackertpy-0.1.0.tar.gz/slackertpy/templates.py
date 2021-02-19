from typing import Dict, List
from slackertpy import builder, blocks


def notification(*, text: str, title: str = None):
    b = builder.MessageBuilder()
    b.add_markdown_text(text)
    if title:
        b.add_header(title)
    return b.build()


def job_start(*, title: str = None, desc: str = None, overview: Dict = None):
    b = builder.MessageBuilder()
    if title:
        b.add_header(title)
    if desc:
        b.add_plain_text(desc)
    if overview:
        _add_section_from_hash(b, overview)

    return b.build()


def job_finish(*, title: str = None, desc: str = None, result: str = None,
               overview: Dict = None):
    b = builder.MessageBuilder()
    if title:
        b.add_header(title)
    if desc:
        b.add_plain_text(desc)
    if result:
        b.add_markdown_text(f"*Result*: {result}")
    if overview:
        _add_section_from_hash(b, overview)

    return b.build()


def job_executed(*, title: str = None, desc: str = None, result: str = None,
                 overview: Dict = None, stats: Dict = None):
    b = builder.MessageBuilder()
    if title:
        b.add_header(title)
    if desc:
        b.add_plain_text(desc)
    if result:
        b.add_markdown_text(f"*Result*: {result}")
    if overview:
        _add_section_from_hash(b, overview)
    if stats:
        _add_section_from_hash(b, stats)

    return b.build()


def job_error(*, title: str, error: str, notify_user_ids: List[str] = None,
              extra: Dict = None, alert_emoji: bool = True):
    b = builder.MessageBuilder()
    header_text = f"ERROR while processing {title}"
    if alert_emoji:
        header_text = f":rotating_light: {header_text}"
    b.add_header(header_text)

    if notify_user_ids:
        b.notify_users(notify_user_ids)
    b.add_divider()
    b.add_markdown_text('*Result*: Fail')
    b.add_markdown_text(f"*Error Output*:\n```{error}```")
    if extra:
        _add_section_from_hash(b, extra)

    return b.build()


def _add_section_from_hash(builder: builder.MessageBuilder, values: Dict):
    builder.add_divider()
    s = blocks.Section.from_dict(values)
    builder.add_section(s)
