# from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, Mapping, Union

import structlog

logger = structlog.get_logger("server")


class Injector:
    def __init__(self, path_to_df: Union[str, Path], loop_data: bool = True) -> None:
        self.path_to_df = Path(path_to_df)
        self.loop = loop_data

    def run(self) -> Iterator[Mapping[str, Any]]:

        import pandas as pd

        try:
            if self.path_to_df.is_dir() or self.path_to_df.suffix == ".parquet":
                data = pd.read_parquet(self.path_to_df)
            else:
                data = pd.read_csv(self.path_to_df)
        except Exception:
            logger.exception("Cannot load data", path=str(self.path_to_df))
            return
        iterator = data.iterrows()
        iterator = (row.to_dict() for _, row in iterator)
        yield from iterator
