"""Storage for tools. That's it for now. 3-30-19"""
import os
import shutil

from tinydb import TinyDB, Query

import exceptions
import tools

HOME = os.path.join(os.path.expanduser('~'), '.toolshed')
the_shed = TinyDB(os.path.join(HOME, 'toolrack.json'))
tool_rack = the_shed.table('tools')


def put(tool: tools.Tool, text: str=None):
    """Adds tool if it doesn't exist, or updates it if it does."""
    tool_rack.upsert(tool.to_dict(), Query().script == tool.script)

    # "text" is a file that should be used to replace the current script
    if text is not None:
        shed_copy = os.path.join(HOME, tool.script)
        try:
            shutil.copyfile(text, shed_copy)
        except FileNotFoundError as e:
            raise exceptions.ScriptNotFound("Text not replaced. Could not copy {} into {} because {} does not exist.."
                                            .format(text, tool.script, text)) from e


def take(script):
    """A getter. Returns the tool specified by the script name, which should be unique."""
    tool_spot = Query()
    result = tool_rack.get(tool_spot.script == script)

    if result:
        return tools.Tool.from_json(result)


def toss(script):
    """Remove tool identified by "script"."""
    tool_spot = Query()
    results = tool_rack.remove(tool_spot.script == script)
    return results


def make(path, invocation, tags):
    """Create a new tool in the shed."""
    _, script = os.path.split(path)

    if tool_rack.contains(Query().script == script):
        raise exceptions.DuplicateTool()

    tool = tools.Tool(script, invocation, tags)
    put(tool, path)


def find(name: str=None, tags: tuple=()):
    """Query tools by name and / or tags."""
    tool = Query()

    if name:
        return tool_rack.search((tool.name == name) & (tool.tags.all(tags)))
    else:
        return tool_rack.search(tool.tags.all(tags))
