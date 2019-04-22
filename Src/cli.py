import argparse
import exceptions
import shed
import utils
import tools


def unknown_command(command: str):
    print('unknown command {}. Available commands are {}.'.format(command, list(command_dispatcher.registry.keys())))


command_dispatcher = utils.Dispatcher()
command_dispatcher.default = unknown_command
command_dispatcher.key = lambda x: x[0]


@command_dispatcher.register('make')
def _(add_args):
    add_parser = argparse.ArgumentParser("Add a tool to the shed")
    add_parser.add_argument("script_path", help="Current path of the tool you want to add. Tool shed will make its "
                                                "own copy.")
    add_parser.add_argument("-i", "--invocation", help="How to invoke this script. E.g. 'python my_awesome_python.py'",
                            default=None)
    add_parser.add_argument("-t", "--tags", nargs="?", help="Searchable tags to know your tools by.")

    args = add_parser.parse_args(add_args[1:])
    shed.make(args.script_path, args.invocation, args.tags)


@command_dispatcher.register('use')
def _(use_args):
    use_parser = argparse.ArgumentParser("User a tool.")
    use_parser.add_argument("script", help="filename (not full path) of tool to execute")
    use_parser.add_argument("-a", "--args", nargs="*", help="arguments to pass to the script", default=[])
    use_parser.add_argument("-i", "--invocation", help="How to invoke the tool", default=None)
    args = use_parser.parse_args(use_args[1:])

    tool = shed.take(args.script)

    if not tool:
        print('Could not find any tool named "{}" in the shed.'.format(args.script))
        return

    if args.invocation:
        tool.invocation = args.invocation

    try:
        tool.invoke(args.args)
    except exceptions.ScriptNotFound:
        print('Whoops. There is a record of {}, however the script could not be found in {}'.format(args.script,
                                                                                                    shed.HOME))
    except exceptions.NoInvocationFound:
        print('Toolshed does not know how to invoke {}. Either add an invocation (use "mod"), or pass one with the '
              '"-i" option.'.format(args.script))


@command_dispatcher.register('mod')
def _(mod_args):
    """"Mod" command. Allows user to update the tool (change script, add / remove tags, etc.)"""
    mod_parser = argparse.ArgumentParser("Modify a tool.")
    mod_parser.add_argument("script", help="Tool to modify.")
    mod_parser.add_argument("-u", "--text", help="Path of file to replace the existing script with.")
    mod_parser.add_argument("-t", "--tags", nargs="+", help="Add tags to tool.")
    mod_parser.add_argument("-i", "--invocation", help="Change invocation.")
    mod_parser.add_argument("-r", "--remove_tags", nargs="+", help="Remove tags from tool.")
    mod_parser.add_argument("-c", "--clear-tags", action="store_true", default=False, help="Remove all tags.")
    mod_parser.add_argument("-d", "--invoke-from", help="Change directory that script is invoked from")

    args = mod_parser.parse_args(mod_args[1:])
    tool = shed.take(args.script)

    if not tool:
        print("No tool \"{}\" found in the shed.".format(args.script))
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

    shed.put(tool, args.text)


@command_dispatcher.register('toss')
def _(toss_args):
    toss_parser = argparse.ArgumentParser("Remove a tool from the shed.")
    toss_parser.add_argument("script", help="name of the tool to remove.")
    args = toss_parser.parse_args(toss_args[1:])

    removed = shed.toss(args.script)
    if not removed:
        print("No script {} exists in the shed. Nothing removed.")


@command_dispatcher.register('find')
def _(find_args):
    find_parser = argparse.ArgumentParser("Search for a tool.")
    find_parser.add_argument('-t', '--tags', nargs='+', help="tags to search for", default=())
    find_parser.add_argument('-n', '--name', help="search for a tool by its name.")

    args = find_parser.parse_args(find_args[1:])
    results = shed.find(name=args.name, tags=args.tags)
    found = sorted(tools.Tool.from_json(r).script for r in results)

    if found:
        print("Results:")
        for f in found:
            print("    {}".format(f))
    else:
        print("No tools found that matched the search criteria.")
