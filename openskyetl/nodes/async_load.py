"""Async Load."""

import asyncio
import logging
from typing import Dict, Optional, Union

import aiomysql

from openskyetl.flow.node import Node
from openskyetl.utils import get_mysql_conn_params

logger = logging.getLogger(__name__)


class AsyncLoad(Node):
    """Async load."""

    SQL = """
        SELECT icao24,
               FROM_UNIXTIME(first_seen, '%Y-%m-%d') AS departure_date,
               FROM_UNIXTIME(first_seen, '%h:%i:%s') AS departure_time,
               est_departure_airport AS source_code,
               est_arrival_airport AS destination_code
          FROM opensky.stage;
    """
    TABLE = "airport"

    conn_params: Dict[str, Union[int, str, Optional[asyncio.AbstractEventLoop]]] = {}

    def run(self) -> None:
        """Run."""
        self.conn_params = get_mysql_conn_params()  # type: ignore
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.to_mysql(self.SQL, self.TABLE, self.conn_params))
        except Exception as exc:
            logger.error("failed to extract data: %s", exc)

    @staticmethod
    async def to_mysql(
        sql: str,
        target_table: str,
        conn_params: Dict[str, Union[int, str, Optional[asyncio.AbstractEventLoop]]],
    ) -> None:
        """Write records from SQL query to a MySQL database.

        Parameters
        ----------
        sql : str
            SQL query
        table : str
            Name of database table to save data
        conn_params : Dict[str, str]
            Connection parameters
        """
        logger.debug("running on database nicknamed `%s`", conn_params.get("db"))
        conn_params["loop"] = asyncio.get_event_loop()
        conn = await aiomysql.connect(**conn_params)
        async with conn.cursor() as cur:
            sql = "INSERT INTO %(table)s " % {"table": target_table} + sql
            await cur.execute(sql)
            await conn.commit()
            logger.info("inserted rows to %s", target_table)
        conn.close()
