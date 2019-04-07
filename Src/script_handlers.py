import logging
import subprocess
import exceptions

logger = logging.getLogger("project")


class ToolTypeDispatcher(object):

    def __init__(self):
        self.registry = {}

    def __call__(self, tool_output):

        assert isinstance(tool_output, subprocess.CompletedProcess)

        try:
            method = self.registry[tool_output.args[0]]
        except KeyError:
            method = self.default_call

        return method(tool_output)

    def register(self, script_type):
        def decorator(method):
            self.registry[script_type] = method
            return method

        return decorator

    @staticmethod
    def default_call(tool_output):
        logger.debug('ToolTypeDispatcher.default_call input={}'.format(tool_output))
        return tool_output


handle_output = ToolTypeDispatcher()


@handle_output.register('python')
def _(output):
    logger.debug('python handler: subprocess output: {}'.format(output))
    if output.returncode == 2:
        raise exceptions.ScriptNotFound()
    return output


@handle_output.register('sh')
def _(output):
    logger.debug('bash handler: subprocess output: {}'.format(output))
    if output.returncode == 127:
        raise exceptions.ScriptNotFound()
    return output
