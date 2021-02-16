#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

import fire
import os
import configparser
import prompt_toolkit
from prompt_toolkit import styles
from prompt_toolkit import formatted_text
import pathlib

__all__ = ["CLI"]

PROMPT_STYLE = styles.Style.from_dict(
    {
        # Prompt.
        "main": "ansibrightyellow",
    }
)


class CLI:
    def init(self, api_key: str = None):
        """Configures the Pinecone client.

        Usage:

        .. code-block:: bash

            pinecone init --api_key=YOUR_API_KEY

        :param api_key: your Pinecone API key
        """
        # Prompt for inputs
        session = prompt_toolkit.PromptSession()
        if not api_key:
            api_key = session.prompt(
                formatted_text.HTML("<main>Pinecone API key: </main>"),
                style=PROMPT_STYLE,
                default=os.getenv("PINECONE_API_KEY", ""),
            )
        # Construct config
        config = configparser.ConfigParser()
        config["default"] = {
            "api_key": api_key,
        }
        config["default"] = {key: val for key, val in config["default"].items() if val}
        # Write config file
        with pathlib.Path.home().joinpath(".pinecone").open("w") as configfile:
            config.write(configfile)


def main():
    try:
        fire.Fire(CLI)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
