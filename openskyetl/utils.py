"""Utils."""

import logging
import os
import time
from typing import Any, Callable, Dict, Union

logger = logging.getLogger(__name__)


def get_mysql_conn_params() -> Dict[str, Union[int, str]]:
    """Get connection parameters."""
    return {
        "host": str(os.environ["MYSQL_HOST"]),
        "port": int(os.environ["MYSQL_TCP_PORT"]),
        "user": str(os.environ["MYSQL_USER"]),
        "password": str(os.environ["MYSQL_ROOT_PASSWORD"]),
        "db": str(os.environ["MYSQL_DATABASE"]),
    }


def measure_time(func: Callable[[], Any]) -> Callable[[], Any]:
    """Measure the time of execution decorator."""

    def time_it(*args: str, **kwargs: str) -> None:
        start_time = time.time()
        func(*args, **kwargs)
        logger.info("`%s` running time is %s seconds", func.__name__, time.time() - start_time)

    return time_it


def to_snake_case(str_: str) -> str:
    """Convert to snake_case from camelCase."""
    return "".join(["_" + i.lower() if i.isupper() else i for i in str_]).lstrip("_")
