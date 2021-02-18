import json

from typing import Dict

import requests

from hycli.commons.error_handling import handle_status_code


@handle_status_code
def request_token(token_endpoint, username, password):
    """ Request invoice extractor API token """
    response = requests.post(
        url=token_endpoint,
        data={
            "username": username,
            "password": password,
            "grant_type": "password",
            "client_id": "extractionapi",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response.raise_for_status()
    return response.json()["access_token"]


@handle_status_code
def extract_invoice(
    file,
    url,
    content_type,
    token,
    headers: Dict = {},
    params: Dict = {},
    timeout: int = 1800,
):
    """ Request invoice extractor """
    if "Content-Type" in headers:
        content_type = headers["Content-Type"]
        if headers["Content-Type"] == "application/vnd.hypatos.ocr+json":
            file = json.dumps(json.loads(file).get("ocr", []))

    params.setdefault("ignoreNull", "false")
    headers.setdefault("Content-Type", content_type)
    headers.setdefault("Authorization", f"Bearer {token}")

    response = requests.post(
        url=url, data=file, params=params, timeout=timeout, headers=headers
    )

    response.raise_for_status()
    return response.json()
