"""Storage for tools. That's it for now. 3-30-19"""
import os
import shutil

import tinydb

import toolshed.exceptions as exceptions
import toolshed.loggers as loggers
import toolshed.tools as tools


class Shed:
    """Implements a singleton pattern per https://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html,
    hence the internal class with the dunder prefix. This class just ensures that there is only a single instance of the
    __Shed class, which does all the actual lifting. All attribute references (methods, members, etc) are fowarded to
    the single __Shed instance by overriding __getattr__ to call getattr on the singleton."""

    class __Shed:
        def __init__(self, home: str=None):
            """Initialize the shed
            :param home: path of the home directory that shed will use for storing scripts & metadata."""

            self._home = home or os.path.join(os.path.expanduser('~'), '.toolshed')

            try:
                os.makedirs(self._home, exist_ok=True)
            except Exception as e:
                raise exceptions.InvalidHomeDirectory('Can\'t find or create home directory "{}".'.format(self._home))\
                    from e

            self._db = tinydb.TinyDB(os.path.join(self._home, 'toolrack.json'))
            self._tool_rack = self._db.table('tools')

        def put(self, tool: tools.Tool, text: str=None):
            """Adds tool if it doesn't exist, or updates it if it does."""
            logger = loggers.get_child_logger(__name__, Shed.__name__, self.__class__.__name__, self.put.__name__)
            logger.debug("Upserting with the arguments: tool={}; text={}".format(tool, text))
            self._tool_rack.upsert(tool.to_dict(), tinydb.Query().script == tool.script)
            logger.debug("Finished upsert.")

            # "text" is a file that should be used to replace the current script
            if text is not None:
                shed_copy = os.path.join(self._home, tool.script)
                try:
                    shutil.copyfile(text, shed_copy)
                except FileNotFoundError as e:
                    raise exceptions.ScriptNotFound(
                        "Text not replaced. Could not copy {} into {} because {} does not exist..".format(
                            text, tool.script, text)) from e

        def take(self, script):
            """A getter. Returns the tool specified by the script name, which should be unique."""
            tool_spot = tinydb.Query()
            result = self._tool_rack.get(tool_spot.script == script)

            if result:
                return tools.Tool.from_json(result)

        def toss(self, script):
            """Remove tool identified by "script"."""
            tool_spot = tinydb.Query()
            results = self._tool_rack.remove(tool_spot.script == script)
            return results

        def make(self, path, invocation, tags):
            """Create a new tool in the shed."""
            _, script = os.path.split(path)

            if self._tool_rack.contains(tinydb.Query().script == script):
                raise exceptions.DuplicateTool()

            tool = tools.Tool(script, invocation, tags)
            self.put(tool, path)

        def find(self, name: str=None, tags: tuple=()):
            """Query tools by name and / or tags."""
            logger = loggers.get_child_logger(__name__, Shed.__name__, self.__class__.__name__, self.put.__name__)
            tool = tinydb.Query()

            if name:
                logger.debug('Recieved name argument. Searching for: name={}, tags={}'.format(name, tags))
                return self._tool_rack.search((tool.name == name) & (tool.tags.all(tags)))
            else:
                logger.debug('Did not recieve name argument. Searching for: tags={}'.format(tags))
                return self._tool_rack.search(tool.tags.all(tags))

        def close(self):
            self._db.close()

        @property
        def home(self):
            return self._home

        @home.setter
        def home(self, _home: str):
            if _home == self._home:
                return

            self._db.close()
            self._home = _home

            try:
                os.makedirs(self._home, exist_ok=True)
            except Exception as e:
                raise exceptions.InvalidHomeDirectory('Can\'nt find or create home directory "{}".'.format(self._home))\
                    from e

            self._db = tinydb.TinyDB(os.path.join(self._home, 'toolrack.json'))
            self._tool_rack = self._db.table('tools')

    __singleton = None

    def __init__(self, home: str=None):
        if not Shed.__singleton:
            Shed.__singleton = Shed.__Shed(home)
        else:
            Shed.__singleton.home = home

    def __getattr__(self, item):
        return getattr(self.__singleton, item)
