"""
Tool represents some kind of code utility. It should be executable. That's it for now. 3-30-19
"""
import os
import shed
import json
import script_handlers
import subprocess
import logging
import exceptions

logger = logging.getLogger("project")


class Tool:

    def __init__(self, script, invocation, invoke_from=None, tags=None):
        self._script = script
        self.invocation = invocation
        self._invoke_from = invoke_from or shed.HOME
        self.tags = tags or []

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

    def invoke(self, args):
        try:
            os.chdir(self._invoke_from)
        except FileNotFoundError as e:
            raise exceptions.InvokeDirectoryNotFound() from e

        script_path = os.path.join(shed.HOME, self._script)
        return script_handlers.handle_output(subprocess.run([self.invocation, script_path] + args.split(' ')))

    def to_json(self):
        return {
            'invoke_from': self._invoke_from,
            'script': self._script,
            'invocation': self.invocation
        }

    @staticmethod
    def from_json(json_object=str):
        members = json.loads(json_object)

        invocation = members.get('invocation', None)
        script = members.get('script', None)
        invoke_from = members.get('invoke_from', None)

        return Tool(script, invocation, invoke_from)
