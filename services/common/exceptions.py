class BaseServiceException(Exception):
    default_message = 'An unknown error occurred.'

    def __init__(self, message=None):
        self.message = message or self.default_message
