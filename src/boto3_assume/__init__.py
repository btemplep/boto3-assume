"""
"""

__version__ = "0.2.0"
__all__ = [
    "assume_role_session",
    "assume_role",
    "Boto3AssumeError",
    "ForbiddenKWArgError",
    "MissingKWArgError"
]

from boto3_assume.core import assume_role_session, assume_role
from boto3_assume.exceptions import Boto3AssumeError, ForbiddenKWArgError, MissingKWArgError

try:
    from boto3_assume.aio_core import assume_role_aio_session
    __all__.append("assume_role_aio_session")
except ModuleNotFoundError as error: # pragma: no cover
    pass
