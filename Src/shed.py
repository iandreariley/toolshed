"""Storage for tools. That's it for now. 3-30-19"""
import os
import shutil

import tinydb

import exceptions
import loggers
import tools


"""Module initialization"""
module_logger = loggers.get_child_logger(__name__)

# Create home directory if it doesn't exist
HOME = os.path.join(os.path.expanduser('~'), '.toolshed')

if not os.path.exists(HOME):
    module_logger.debug("Creating toolshed home folder \"{}\".".format(HOME))
    os.makedirs(HOME, exist_ok=True)
    module_logger.debug("Finished creating toolshed home folder.")

# Setup database
module_logger.debug("Setting up database and tool table.")
the_shed = tinydb.TinyDB(os.path.join(HOME, 'toolrack.json'))
tool_rack = the_shed.table('tools')
module_logger.debug("Finished setting up database and tool table.")


def put(tool: tools.Tool, text: str=None):
    """Adds tool if it doesn't exist, or updates it if it does."""
    logger = loggers.get_child_logger(__name__, put.__name__)
    logger.debug("Upserting with the arguments: tool={}; text={}".format(tool, text))
    tool_rack.upsert(tool.to_dict(), tinydb.Query().script == tool.script)
    logger.debug("Finished upsert.")

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
    tool_spot = tinydb.Query()
    result = tool_rack.get(tool_spot.script == script)

    if result:
        return tools.Tool.from_json(result)


def toss(script):
    """Remove tool identified by "script"."""
    tool_spot = tinydb.Query()
    results = tool_rack.remove(tool_spot.script == script)
    return results


def make(path, invocation, tags):
    """Create a new tool in the shed."""
    _, script = os.path.split(path)

    if tool_rack.contains(tinydb.Query().script == script):
        raise exceptions.DuplicateTool()

    tool = tools.Tool(script, invocation, tags)
    put(tool, path)


def find(name: str=None, tags: tuple=()):
    """Query tools by name and / or tags."""
    logger = loggers.get_child_logger(__name__, find.__name__)
    tool = tinydb.Query()

    if name:
        logger.debug('Recieved name argument. Searching for: name={}, tags={}'.format(name, tags))
        return tool_rack.search((tool.name == name) & (tool.tags.all(tags)))
    else:
        logger.debug('Did not recieve name argument. Searching for: tags={}'.format(tags))
        return tool_rack.search(tool.tags.all(tags))
