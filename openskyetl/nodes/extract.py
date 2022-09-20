"""Extract."""

import logging
from typing import Any, Dict, List, Tuple, Union

import mysql.connector
import requests

from openskyetl.flow.node import Node
from openskyetl.utils import get_mysql_conn_params, to_snake_case

logger = logging.getLogger(__name__)


class Extract(Node):
    """Extract."""

    AIRPORTS = ["EGLL", "LFPG", "EHAM"]
    INTERVALS = [1567296000, 1567900800, 1568505600]
    BASE_URL = "https://opensky-network.org/api/flights/departure"

    conn_params: Dict[str, Union[int, str]] = get_mysql_conn_params()

    def run(self) -> None:
        """Run."""
        data: List[Tuple[Any, ...]] = []
        logger.debug("running on database nicknamed `stage`")
        with mysql.connector.connect(**self.conn_params) as conn:
            cur = conn.cursor()
            for begin, end in list(zip(self.INTERVALS, [ts - 86400 for ts in self.INTERVALS[1:]])):
                for airport in self.AIRPORTS:
                    url = "{}?airport={airport}&begin={begin}&end={end}".format(
                        self.BASE_URL, airport=airport, begin=begin, end=end
                    )
                    resp = requests.get(url)
                    data = data + [tuple(row.values()) for row in resp.json()]
            try:
                cols = tuple(to_snake_case(col) for col in resp.json()[0].keys())
                cols_format = " (" + "%s, " * (len(cols) - 1) + "%s) "
                sql = "INSERT INTO stage" + cols_format % cols + "VALUES" + cols_format
                cur.executemany(sql, data)
            except Exception as exc:
                conn.rollback()
                raise RuntimeError("failed to insert records to database rollback") from exc
            conn.commit()
