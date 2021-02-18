"""
Formatting of Slack Messages from Default Message types
"""
from gretel_core.notifications.messages import DefaultMessage, Level


def _slack_context_text(data: dict):
    parts = [f"{k}: {v}" for k, v in data.items()]
    return {
        "type": "plain_text",
        "text": " | ".join(parts),
        "emoji": True
    }


def _slack_section_text(data: dict):
    _out = []
    for k, v in data.items():
        _out.append({
            "type": "mrkdwn",
            "text": f"*{k}*: {v}"
        })
    return _out


_LEVEL_MAP = {
    Level.INFO: ":information_source:",
    Level.WARNING: ":warning:",
    Level.ERROR: ":bangbang:",
    Level.CRITICAL: ":rotating_light:"
}


def from_default(message: DefaultMessage) -> dict:
    blocks = []

    # build the title / header
    blocks.append({
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": message.title,
            "emoji": True
        }
    })

    # add the initial metadata
    if message.header:
        blocks.append({
            "type": "context",
            "elements": [_slack_context_text(message.header)]
        })

    # add ts
    blocks.append({
        "type": "section",
        "fields": [
            {
                "type": "mrkdwn",
                "text": f"*Timestamp*: {message.ts.isoformat() + 'Z'}"
            }
        ]
    })

    level_emoji = _LEVEL_MAP[message.level]

    # add level
    blocks.append({
        "type": "section",
        "fields": [
            {
                "type": "mrkdwn",
                "text": f"*Level*: {message.level.value}  {level_emoji}"
            }
        ]
    })

    # add the main message content
    if message.body:
        blocks.append({
            "type": "section", 
            "fields": _slack_section_text(message.body)
        })

    # divider and footer only if we have a footer
    if message.footer:
        blocks.append({
            "type": "divider"
        })

        blocks.append({
            "type": "context",
            "elements": [_slack_context_text(message.footer)]
        })

    payload = {
        "text": "",
        "blocks": blocks
    }

    return payload
