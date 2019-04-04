import argparse
import logging
import pprint
import sys
from cli import command_dispatcher


actions = {
    'add': 'Add a tool to the shed.',
    'use': 'Use a tool in the shed. Takes arguments that the tool eats.',
    'mod': 'Modify your tool to make it more powerful. Gain 100 xp.',
    'toss': 'Remove a tool from the shed. Like. Forever.'
}


logger = logging.getLogger("project")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


parser = argparse.ArgumentParser("A cool place to store your tools out of the hot sun.")
parser.add_argument('action', help=pprint.pformat(actions), choices=['add', 'use', 'mod', 'toss'])
known_args, unknown_args = parser.parse_known_args()
command_dispatcher(sys.argv[1:])

