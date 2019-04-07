import argparse
import exceptions
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
    use_parser = argparse.ArgumentParser("User a tool.")
    use_parser.add_argument("script", help="filename (not full path) of tool to execute")
    use_parser.add_argument("-a", "--args", nargs="*", help="arguments to pass to the script", default=[])
    args = use_parser.parse_args(use_args[1:])

    tool = shed.take(args.script)
    try:
        tool.invoke(args.args)
    except exceptions.ScriptNotFound:
        print('Whoops. No tool named "{}" in the shed'.format(args.script))


@command_dispatcher.register('mod')
def _(mod_args):
    mod_parser = argparse.ArgumentParser("Modify a tool.")
    mod_parser.add_argument("script", help="Tool to modify.")
    mod_parser.add_argument("-t", "--tags", nargs="+", help="Add tags to tool.")
    mod_parser.add_argument("-i", "--invocation", help="Change invocation.")
    mod_parser.add_argument("-r", "--remove_tags", nargs="+", help="Remove tags from tool.")
    mod_parser.add_argument("-c", "--clear-tags", action="store_true", default=False, help="Remove all tags.")
    mod_parser.add_argument("-d", "--invoke-from", help="Change directory that script is invoked from")

    args = mod_parser.parse_args(mod_args[1:])
    tool = shed.take(args.script)

    if not tool:
        print("No tool \"{}\" found in the shed.")
        return

    if args.tags:
        tool.tags.extend(args.tags)

    if args.invocation:
        tool.invocation = args.invocation

    if args.remove_tags:
        to_remove = set(args.remove_tags)
        tool.tags = [t for t in tool.tags if t not in to_remove]

    if args.clear_tags:
        tool.tags = []

    if args.invoke_from:
        try:
            tool.invoke_from = args.invoke_from
        except exceptions.InvokeDirectoryNotFound:
            print("Invoke-from directory \"{}\" is not a valid directory or does not exist. directory not updated.")

    shed.put(tool)




@command_dispatcher.register('toss')
def _(toss_args):
    pass
