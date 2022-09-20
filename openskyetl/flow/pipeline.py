"""Definition of abstract CLI command."""

import argparse
import logging
import sys
from abc import ABC, abstractmethod
from copy import deepcopy
from typing import List, Type

from openskyetl.flow.node import Node

logger = logging.getLogger(__name__)


class NodeRunError(RuntimeError):
    """Error running the node."""


class Pipeline(ABC):
    """Base class for executables.

    In a child class methods `add_command_arguments`, `add_custom_process`, `add_steps`,
    `get_description`, can be overvritten to implement more specific needs.
    """

    args = None
    nodes: List[Type[Node]] = []

    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description=self.get_description())
        self.parser.add_argument("--debug", action="store_true", help="enable debug output")

    def _run_nodes(self, nodes_to_run: List[Type[Node]], exit_on_error: bool) -> None:
        """Run the given nodes."""
        for node in nodes_to_run:
            logger.info("running node: %s", node.__name__)
            user_config = deepcopy(vars(self.args))
            res = node().process_local(user_config=user_config)
            if res != 0:
                if exit_on_error:
                    logger.critical("node %s returned nonzero (%s): exiting", node.__name__, res)
                    sys.exit(res)
                else:
                    logger.error("node %s returned nonzero (%s)", node.__name__, res)
                    raise NodeRunError
            else:
                logger.info("node %s finished successfully", node.__name__)

    def main(self) -> None:
        """Execute."""
        self.add_command_arguments()
        self.args = self.parser.parse_args()
        try:
            self.add_custom_process()
            self.add_nodes()
            logger.info("running all the nodes")
            self._run_nodes(self.nodes, exit_on_error=not self.args.debug)
        except Exception as exc:
            if not self.args.debug:
                logger.critical("runsteps ended with an error: %s: exiting, exc")
                sys.exit(1)
            else:
                logger.error("runsteps ended with an error: %s", exc)
                raise RuntimeError from exc

    @abstractmethod
    def get_description(self) -> str:
        """Return description used in --help."""

    def add_command_arguments(self) -> None:
        """Add custom CLI arguments to `self.parser`."""

    def add_custom_process(self) -> None:
        """Overwrite to add custom processing of parameters."""

    @abstractmethod
    def add_nodes(self) -> None:
        """In this function `self.nodes` should be definded as an iterable of nodes to be runned."""
