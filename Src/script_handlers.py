import logging

import exceptions
import utils

logger = logging.getLogger("project")


def default_call(tool_output):
    logger.debug('ToolTypeDispatcher.default_call input={}'.format(tool_output))
    return tool_output


def tool_key(tool_output):
    return tool_output.args[0]


handle_output = utils.Dispatcher(tool_key, default_call)


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
