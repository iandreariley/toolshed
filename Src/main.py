import argparse
import logging
import sys

from cli import command_dispatcher


def run():
    logger = logging.getLogger("project")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    parser = argparse.ArgumentParser("A place to save your dev tools so you don't have to make them all over again.")
    actions = command_dispatcher.registry.keys()
    parser.add_argument('action', help='Choose from these actions', choices=list(actions))
    command_dispatcher(sys.argv[1:])

