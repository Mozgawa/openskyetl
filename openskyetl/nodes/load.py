"""Load."""

import logging
from typing import Dict, Union

import mysql.connector

from openskyetl.flow.node import Node
from openskyetl.utils import get_mysql_conn_params

logger = logging.getLogger(__name__)


class Load(Node):
    """Load."""

    SQL = """

        SELECT icao24,
               FROM_UNIXTIME(first_seen, '%Y-%m-%d') AS departure_date,
               FROM_UNIXTIME(first_seen, '%h:%i:%s') AS departure_time,
               est_departure_airport AS source_code,
               est_arrival_airport AS destination_code
          FROM opensky.stage;
    """
    TABLE = "airport"

    conn_params: Dict[str, Union[int, str]] = get_mysql_conn_params()

    def run(self) -> None:
        """Run."""
        self.to_mysql(self.SQL, self.TABLE, self.conn_params)

    def to_mysql(self, sql: str, table: str, conn_params: Dict[str, Union[int, str]]) -> None:
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
        logger.debug("running on database nicknamed `%s`", conn_params.get("dbname"))
        with mysql.connector.connect(**conn_params) as conn:
            cur = conn.cursor()
            try:
                sql = "INSERT INTO %(table)s " % {"table": table} + sql
                cur.execute(sql)
                logger.info("inserted rows to %s", table)
                conn.commit()
            except Exception as exc:
                conn.rollback()
                logger.error("failed to insert records to database rollback: %s", exc)
