"""Storage for tools. That's it for now. 3-30-19"""
import os
import tools
import exceptions
import shutil
from tinydb import TinyDB, Query

HOME = os.path.join(os.path.expanduser('~'), '.toolshed')
the_shed = TinyDB(os.path.join(HOME, 'toolrack.json'))
tool_rack = the_shed.table('tools')


def put(tool: tools.Tool, text: str=None):
    tool_spot = Query()
    tool_rack.upsert(tool.to_dict(), tool_spot.script == tool.script)

    # "text" is a file that should be used to replace the current script
    if text is not None:
        shed_copy = os.path.join(HOME, tool.script)
        try:
            shutil.copyfile(text, shed_copy)
        except FileNotFoundError as e:
            raise exceptions.ScriptNotFound("Text not replaced. Could not copy {} into {} because {} does not exist.."
                                            .format(text, tool.script, text)) from e


def take(script):
    tool_spot = Query()
    results = tool_rack.search(tool_spot.script == script)

    if len(results) > 1:
        raise exceptions.DuplicateTool()

    try:
        return tools.Tool.from_json(results[0])
    except IndexError:
        return None


def toss(script):
    tool_spot = Query()
    results = tool_rack.remove(tool_spot.script == script)
    return results


def new_tool(path, invocation, tags):
    if not os.path.isfile(path):
        raise exceptions.InvalidTool()

    _, script = os.path.split(path)
    shed_copy = os.path.join(HOME, script)
    shutil.copyfile(path, shed_copy)

    # TODO: Check if tags are in known tags.

    tool = tools.Tool(script, invocation, tags)
    put(tool)
