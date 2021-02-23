from typing import List
import requests

from magicapi import g


def send_email(text: str, recipients: List[str], subject: str = "", reply_to: str = None):
    data = {
        "from": f"{g.settings.mailgun_sender_name} <{g.settings.mailgun_sender_email}>",
        "to": recipients,
        "subject": subject,
        "text": text,
    }
    if "html" in data["text"]:
        data["html"] = data["text"]
        del data["text"]
    if reply_to:
        data['h:Reply-To'] = reply_to
    return requests.post(
        f"https://api.mailgun.net/v3/{g.settings.mailgun_domain_name}/messages",
        auth=("api", g.settings.mailgun_private_api_key),
        data=data,
    )


if __name__ == "__main__":
    resp = send_email(
        recipients=["kellycup8@aim.com"], text="jey man", subject="yessir"
    )
    print("resp content", resp.content)
