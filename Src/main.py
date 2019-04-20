import argparse
import logging
import pprint
import sys
from cli import command_dispatcher


logger = logging.getLogger("project")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

parser = argparse.ArgumentParser("A cool place to store your tools out of the hot sun.")
actions = command_dispatcher.registry.keys()
parser.add_argument('action', help=pprint.pformat(actions), choices=actions)
known_args, unknown_args = parser.parse_known_args()
command_dispatcher(sys.argv[1:])

