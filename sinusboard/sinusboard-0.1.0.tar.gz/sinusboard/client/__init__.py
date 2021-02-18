"""Initialise the client for SinusBot operations."""

from typing import Final

from requests import Session

session = Session()

AUTHORIZATION: Final[dict[str, str]] = {
    "botId": "68f1f867-32f7-431c-af97-7604ee4dcbf3",
    "password": "Meme",
    "username": "jerbob",
}
API_ROOT: Final[str] = "http://ix1game01.infernolan.co.uk:8087/api/v1/bot"
PLAY: Final[str] = f"{API_ROOT}/i/82faa775-298d-4c9f-9827-4dd8b91399b0/play/byId/{{uuid}}"
TOKEN: Final[str] = session.post(f"{API_ROOT}/login", json=AUTHORIZATION).json().get("token")

CLIPS: Final[list[dict[str, str]]] = [
    {"name": "Certified Hood Classic", "uuid": "cdd5d14e-326e-4ede-ab77-a59483b06db9"},
    {"name": "See ya man", "uuid": "655907d2-c9b8-4eec-bd40-fdbf670a2921"},
    {"name": "Among Drip", "uuid": "02c48548-a728-4e4d-9288-52b1a72c0e57"},
    {"name": "Vine Thud", "uuid": "c979bcfb-4be2-4378-b03b-351261fe9ef0"},
    {"name": "Ring ding ding", "uuid": "b00bdfd6-b258-433f-9897-9357b5bb2aab"},
    {"name": "Dream", "uuid": "f84cffbe-5cfc-4ddf-b8d2-e6e4c3ab6c50"},
    {"name": "Ultra Instinct", "uuid": "434d85ad-25b9-4070-b4c6-0582dccefbaa"},
]

session.headers["Authorization"] = f"Bearer {TOKEN}"


def play_clip(uuid: str) -> None:
    """Play the specified clip using SinusBot."""
    return session.post(PLAY.format(uuid=uuid)).json()
