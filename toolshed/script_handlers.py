import logging

import toolshed

logger = logging.getLogger("project")


def default_call(tool_output):
    """Simply logs the output if no handler is specified"""
    logger.debug('ToolTypeDispatcher.default_call input={}'.format(tool_output))
    return tool_output


def tool_key(tool_output):
    """The key of the handler is always the first argument, which we assume is the invocation (e.g. python)"""
    return tool_output.args[0]


handle_output = toolshed.Dispatcher(tool_key, default_call)


@handle_output.register('python')
def _(output):
    """Handle the output of a python process."""
    logger.debug('python handler: subprocess output: {}'.format(output))
    if output.returncode == 2:
        raise toolshed.ScriptNotFound()
    return output


@handle_output.register('sh')
def _(output):
    """Handle the output of a bash process."""
    logger.debug('bash handler: subprocess output: {}'.format(output))
    if output.returncode == 127:
        raise toolshed.ScriptNotFound()
    return output
