import argparse
import sys

import cli
import loggers


def run():
    logger = loggers.get_module_logger(__name__)
    parser = argparse.ArgumentParser("A place to save your dev tools so you don't have to make them all over again.")
    actions = cli.command_dispatcher.registry.keys()

    logger.debug("Parsing arguments in {}.{}".format(__name__, run.__name__))
    parser.add_argument('action', help='Choose from these actions', choices=list(actions))
    cli.command_dispatcher(sys.argv[1:])
