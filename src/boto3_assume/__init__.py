"""
"""

__version__ = "0.1.0"
__all__ = []


try:
    from boto3_assume.core import assume_role_session
    __all__.append("assume_role_session")
except ModuleNotFoundError as error: # pragma: no cover
    pass
try:
    from boto3_assume.aio_core import assume_role_aio_session
    __all__.append("assume_role_aio_session")
except ModuleNotFoundError as error: # pragma: no cover
    pass
