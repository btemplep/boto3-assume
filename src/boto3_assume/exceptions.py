"""boto3-assume exceptions
"""
__all__ = [
    "Boto3AssumeError",
    "ForbiddenKWArgError",
    "MissingKWArgError"
]
class Boto3AssumeError(Exception):
    """Base exception for boto3-assume
    """
    pass

class ForbiddenKWArgError(Boto3AssumeError):
    pass

class MissingKWArgError(Boto3AssumeError):
    pass