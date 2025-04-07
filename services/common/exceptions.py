class BaseAppException(Exception):
    default_message = "An unknown error occurred."

    def __init__(self, message=None):
        message = message or self.default_message

        self.message = f"{self.__class__.__name__}({message})"


class BaseSchemaException(BaseAppException): ...


class BaseServiceException(BaseAppException): ...
