from wallstreet.exceptions.base_exceptions import *


class ImproperlyConfigured(Error):
    """
    Exception raised when the configuration is not valid.

    Attributes:
        message -- explanation of the error
    """
