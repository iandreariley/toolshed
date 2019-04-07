"""Storage for tools. That's it for now. 3-30-19"""
import os
import tools
import exceptions
import shutil
from tinydb import TinyDB, Query

HOME = os.path.join(os.path.expanduser('~'), '.toolshed')
the_shed = TinyDB(os.path.join(HOME, 'toolrack.json'))
tool_rack = the_shed.table('tools')


def put(tool: tools.Tool):
    tool_spot = Query()
    tool_rack.upsert(tool.to_dict(), tool_spot.script == tool.script)


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
    results = tool_rack.search(tool_spot.script == script)
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
