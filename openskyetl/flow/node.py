"""Abstract class for a pipeline node.

Usage example to write own node:

    from flow.node import Node

    class HelloWorld(Node):
        def run(self):
            print("Hello World!")

Need to override the `run()` method.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class Node(ABC):
    """Abstract class for defining an pipeline processing node."""

    params = None
    _returncode = None

    @abstractmethod
    def run(self) -> None:
        """Workflow definition."""

    def _init_params(self, user_config: Optional[Dict[Any, Any]]) -> None:
        """Initialize parameters."""
        self.params = user_config

    def _init_custom(self) -> None:
        """Initialize custom implementations of the Node class."""
        logger.debug("no custom init function for Node defined")

    def _common_pre_run(self, user_config: Optional[Dict[Any, Any]]) -> None:
        self._init_params(user_config)
        self._init_custom()

    def _deinit_exitcode(self, returncode: Any) -> None:
        """Process exitcode.

        Result written to `self._returncode`.
        """
        if returncode is None:
            norm_rc = 0
        elif isinstance(returncode, bool):
            norm_rc = 0 if returncode else 1
        else:
            try:
                returncode = int(returncode)
                if returncode < 0 or returncode > 255:
                    raise ValueError()
            except ValueError as err:
                raise RuntimeError(
                    "run() method returns an unknown type or int outside range"
                ) from err
            norm_rc = returncode
        self._returncode = norm_rc

    def _deinit_custom(self) -> None:
        """Deinitialize custom implementations of the Node class."""
        logger.debug("no custom deinit function for Node defined")

    def _common_post_run(self, returncode: Any) -> None:
        """Exit the program."""
        self._deinit_exitcode(returncode)
        self._deinit_custom()

    def process_local(self, user_config: Optional[Dict[Any, Any]] = None) -> Optional[int]:
        """Wrap execution of `run()` when running locally.

        Parameters
        ----------
        user_config : dict
            Configuration parameters from the user

        Returns
        -------
        int
            Exitcode, 0 for success, nonzero (up to 255) for failure
        """
        try:
            self._common_pre_run(user_config)
            logger.info("running locally, a step will be run")
            res = self.run()
        except Exception as exc:
            logger.error("node %s ended with an error: %s", type(self).__name__, exc)
            res = 1
        try:
            self._common_post_run(returncode=res)
            return self._returncode
        except Exception as exc:
            logger.error("post run ended with an error: %s", exc)
            return 1
