import argparse
import os
import sys

import toolshed.cli as cli
import toolshed.loggers as loggers


def run():
    logger = loggers.get_child_logger(__name__, run.__name__)
    parser = argparse.ArgumentParser("A place to save your dev tools so you don't have to make them all over again.")
    actions = cli.command_dispatcher.registry.keys()
    logger.debug("Executing from {}".format(os.getcwd()))

    args = sys.argv[1:]
    logger.debug("Parsing arguments: {}".format(args))
    parser.add_argument('action', help='Choose from these actions', choices=list(actions))
    cli.command_dispatcher(args)


run()
