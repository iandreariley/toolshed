"""
Tool represents some kind of code utility. It should be executable. That's it for now. 3-30-19
"""
import logging
import os
import subprocess

import toolshed.shed as shed
import toolshed.script_handlers as script_handlers
import toolshed.exceptions as exceptions

logger = logging.getLogger("project")


class Tool:

    def __init__(self, script, invocation=None, invoke_from=None, tags=None):
        self._script = script
        self.invocation = invocation
        self._invoke_from = invoke_from or shed.HOME
        self.tags = tags or []

    def invoke(self, args):
        """Invokes the tool in a subprocess with the given args."""

        try:
            os.chdir(self._invoke_from)
        except FileNotFoundError as e:
            raise exceptions.InvokeDirectoryNotFound() from e

        script_path = os.path.join(shed.HOME, self._script)

        if not os.path.isfile(script_path):
            raise exceptions.ScriptNotFound()

        if not self.invocation:
            raise exceptions.NoInvocationFound()

        return script_handlers.handle_output(subprocess.run([self.invocation, script_path] + args))

    def to_dict(self):
        return {
            'invoke_from': self._invoke_from,
            'script': self._script,
            'invocation': self.invocation,
            'tags': self.tags
        }

    @property
    def invoke_from(self):
        return self._invoke_from

    @invoke_from.setter
    def invoke_from(self, invoke_from):
        if not os.path.isdir(invoke_from):
            raise exceptions.InvokeDirectoryNotFound()
        self._invoke_from = invoke_from

    @property
    def script(self):
        return self._script

    @script.setter
    def script(self, script):
        if not os.path.exists(os.path.join(shed.HOME, script)):
            raise exceptions.ScriptNotFound()
        self._script = script

    @staticmethod
    def from_json(members):

        return Tool(
            members['script'],
            members['invocation'],
            members['invoke_from'],
            members['tags']
        )
