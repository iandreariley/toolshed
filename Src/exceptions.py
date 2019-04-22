class InvokeDirectoryNotFound(FileNotFoundError):
    pass


class ScriptNotFound(FileNotFoundError):
    pass


class DuplicateTool(Exception):
    pass


class InvalidTool(ValueError):
    pass


class InvalidInvocation(ValueError):
    pass


class NoInvocationFound(TypeError):
    pass
