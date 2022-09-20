"""Async extract."""

import asyncio
import logging
from typing import Any, Dict, List, Union

import aiohttp
import aiomysql
import mysql.connector

from openskyetl.flow.node import Node
from openskyetl.utils import get_mysql_conn_params, to_snake_case

logger = logging.getLogger(__name__)


class AsyncExtract(Node):
    """Async extract."""

    AIRPORTS = ["EGLL", "LFPG", "EHAM"]
    TIMESTAMPS = [1567296000, 1567900800, 1568505600]
    BASE_URL = "https://opensky-network.org/api/flights/departure"
    TABLE = "stage"

    conn_params: Dict[str, Union[int, str, asyncio.AbstractEventLoop]] = {}

    def _mysql_auth_workaround(self) -> None:
        self.conn_params = get_mysql_conn_params()  # type: ignore
        self.conn_params["database"] = self.conn_params["db"]
        del self.conn_params["db"]
        with mysql.connector.connect(**self.conn_params):
            pass
        self.conn_params["db"] = self.conn_params["database"]
        del self.conn_params["database"]

    def _init_custom(self) -> None:
        self._mysql_auth_workaround()
        self.conn_params = get_mysql_conn_params()  # type: ignore
        loop = asyncio.get_event_loop()
        self.conn_params["loop"] = loop
        loop.run_until_complete(self._truncate())

    async def _truncate(self) -> None:
        conn = await aiomysql.connect(**self.conn_params)
        async with conn.cursor() as cur:
            sql = "TRUNCATE %s;" % (self.TABLE,)
            await cur.execute(sql)
            await conn.commit()
            conn.close()

    def run(self) -> None:
        """Run."""
        params_list = [
            {"airport": airport, "begin": begin, "end": end}
            for airport in self.AIRPORTS
            for begin, end in list(zip(self.TIMESTAMPS, [ts - 86400 for ts in self.TIMESTAMPS[1:]]))
        ]
        self._extract_many(params_list)

    async def _get_airport(self, params: Dict[str, Union[str, object]]) -> Any:
        url = "{}?airport={airport}&begin={begin}&end={end}".format(self.BASE_URL, **params)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()
                return data

    async def _extract_one(self, params: Dict[str, Union[str, object]]) -> None:
        data = await self._get_airport(params)
        await self._stage(data)

    def _extract_many(self, params_list: List[Dict[str, Union[str, object]]]) -> None:
        loop = asyncio.get_event_loop()
        try:
            to_do = [self._extract_one(params) for params in params_list]
            wait_coro = asyncio.wait(to_do)
            loop.run_until_complete(wait_coro)
        except Exception as exc:
            logger.error("failed to extract data: %s", exc)

    async def _stage(self, data: List[Dict[str, Union[int, str]]]) -> None:
        self.conn_params["loop"] = asyncio.get_event_loop()
        cols = tuple(to_snake_case(col) for col in data[0].keys())
        cols_format = " (" + "%s, " * (len(cols) - 1) + "%s) "
        conn = await aiomysql.connect(**self.conn_params)
        try:
            async with conn.cursor() as cur:
                sql = "INSERT INTO %s" % (self.TABLE,) + cols_format % cols + "VALUES" + cols_format
                await cur.executemany(sql, [tuple(row.values()) for row in data])
                await conn.commit()
        except Exception as exc:
            await conn.rollback()
            logger.error("failed to insert records to database rollback: %s", exc)
        finally:
            conn.close()
