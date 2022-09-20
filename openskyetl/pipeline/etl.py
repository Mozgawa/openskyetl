"""ETL."""

from typing import List, Type

from openskyetl.flow.node import Node
from openskyetl.flow.pipeline import Pipeline
from openskyetl.nodes.async_extract import AsyncExtract
from openskyetl.nodes.async_load import AsyncLoad
from openskyetl.nodes.extract import Extract
from openskyetl.nodes.load import Load
from openskyetl.utils import measure_time


class ETL(Pipeline):
    """ETL."""

    nodes: List[Type[Node]] = []

    def get_description(self) -> str:
        """Return description used in --help."""
        return "ETL."

    def add_nodes(self) -> None:
        """Configure nodes to run."""
        if self.args.async_run:  # type: ignore
            self.nodes = [AsyncExtract, AsyncLoad]
        else:
            self.nodes = [Extract, Load]

    def add_command_arguments(self) -> None:
        """Add command line arguments."""
        self.parser.add_argument("-a", "--async-run", action="store_true", help="run async")


@measure_time
def main() -> None:
    """Exposes the class."""
    etl = ETL()
    etl.main()
