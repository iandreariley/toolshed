import argparse
import os
import sys

import toolshed


def run():
    logger = toolshed.get_child_logger(__name__, run.__name__)
    parser = argparse.ArgumentParser("A place to save your dev tools so you don't have to make them all over again.")
    actions = toolshed.command_dispatcher.registry.keys()
    logger.debug("Executing from {}".format(os.getcwd()))

    args = sys.argv[1:]
    logger.debug("Parsing arguments: {}".format(args))
    parser.add_argument('action', help='Choose from these actions', choices=list(actions))
    parser.parse_args(sys.argv[1:2])
    toolshed.command_dispatcher(sys.argv[1:])

