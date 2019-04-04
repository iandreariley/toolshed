import argparse
import shed
import utils


def unknown_command(command: str):
    print('unknown command {}. Available commands are {}.'.format(command, list(command_dispatcher.registry.keys())))


command_dispatcher = utils.Dispatcher()
command_dispatcher.default = unknown_command
command_dispatcher.key = lambda x: x[0]


@command_dispatcher.register('add')
def _(add_args):
    add_parser = argparse.ArgumentParser("Add a tool to the shed")
    add_parser.add_argument("script_path", help="Current path of the tool you want to add. Tool shed will make its "
                                                "own copy.")
    add_parser.add_argument("invocation", help="How to invoke this script. E.g. 'python my_awesome_python.py'")
    add_parser.add_argument("-t", "--tags", nargs="?", help="Searchable tags to know your tools by.")

    args = add_parser.parse_args(add_args[1:])
    shed.new_tool(args.script_path, args.invocation, args.tags)


@command_dispatcher.register('use')
def _(use_args):
    pass


@command_dispatcher.register('mod')
def _(mod_args):
    pass


@command_dispatcher.register('toss')
def _(toss_args):
    pass
