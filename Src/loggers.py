import logging
import sys


# Set up project logger.
project_logger = logging.getLogger("toolshed")
project_logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
project_logger.addHandler(handler)
module_logger = logging.getLogger('toolshed.' + __name__)
module_logger.debug('finished logging setup.')


def get_child_logger(*names: str):
    """Returns a child logger of the project-level logger with the name toolshed.<name>."""
    return logging.getLogger("toolshed." + '.'.join(names))


# def log_inputs(logger: logging.Logger, log_level: int=logging.DEBUG):
#     """Logs inputs / outputs to the logger with the given name."""
#
#     def decorator(method):
#         nonlocal logger, log_level
#         logger.log(log_level, "")