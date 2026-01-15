
from typing import Any, Dict, Optional
import warnings

import boto3
from botocore.credentials import DeferredRefreshableCredentials

from boto3_assume.assume_refresh import AssumeRefresh
from boto3_assume.exceptions import ForbiddenKWArgError, MissingKWArgError


def assume_role_session(
    source_session: boto3.Session,
    RoleArn: str, 
    RoleSessionName: str, 
    sts_client_kwargs: Optional[Dict[str, Any]] = None,
    assume_role_kwargs: Optional[Dict[str, Any]] = None
) -> boto3.Session:
    """**DEPRECATED** - Please see the new ``assume_role`` function. 
    
    Generate an assume role ``boto3`` session, that will automatically refresh credentials.

    Parameters
    ----------
    source_session : boto3.Session
        Source session to assume the role from.
    RoleArn : str
        ARN of the role to assume.
    RoleSessionName : str
        The session name to pass in ```sts_client.assume_role()`` .
    sts_client_kwargs : Optional[Dict[str, Any]], optional
        Extra kwargs to pass when creating the STS client, by default None
    assume_role_kwargs : Optional[Dict[str, Any]], optional
        Extra kwargs to pass when calling assume role on the STS client, by default None

    Returns
    -------
    boto3.Session
        The assumed role session.
    """
    warnings.warn(
        "The `assume_role_session` function is deprecated and will be removed.  Please use the `assume_role` function.",
        category=DeprecationWarning,
        stacklevel=2
    )
    if sts_client_kwargs is None:
        sts_client_kwargs = {}
    
    if assume_role_kwargs is None:
        assume_role_kwargs = {}
    
    assume_role_kwargs['RoleArn'] = RoleArn
    assume_role_kwargs['RoleSessionName'] = RoleSessionName
    assume_sess = boto3.Session()
    assume_sess._session._credentials = DeferredRefreshableCredentials(
        refresh_using=AssumeRefresh(
            source_session=source_session,
            sts_client_kwargs=sts_client_kwargs,
            assume_role_kwargs=assume_role_kwargs
        ).refresh,
        method="sts-assume-role"
    )
    
    return assume_sess


def _check_forbidden_keys(name: str, kwargs: dict, forbidden_keys: list) -> None:
    for key in kwargs:
        if key in forbidden_keys:
            raise ForbiddenKWArgError(f"{name} cannot contain the '{key}' key when used with boto3-assume.")


def assume_role(
    source_session: boto3.Session,
    assume_role_kwargs: Dict[str, Any],
    sts_client_kwargs: Dict[str, Any] = None,
    target_session_kwargs: Dict[str, Any] = None
) -> boto3.Session:
    """Generate an assume role ``boto3`` session, that will automatically refresh credentials.

    Parameters
    ----------
    source_session : boto3.Session
        Source session to assume the role from. Must be a session that will automatically refresh its own credentials.
    assume_role_kwargs : Dict[str, Any], default=None
        Keyword arguments to pass when calling `assume_role <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/assume_role.html>`_. with a boto3 STS client.
        Must at least provide ``RoleArn`` and ``RoleSessionName`` as outlined in the boto3 docs.
    sts_client_kwargs : Dict[str, Any], default=None
        Kwargs to pass when creating the `boto3 low level client <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.client>`_. for `STS client <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html>`_.
        By default only the service argument will be passed as ``"sts"``. 
        Note that you should not pass in the ``service_name`` or credentials here. 
    target_session_kwargs : Dict[str, Any], default=None
        Keyword arguments to pass when creating a the new target `boto3 Session <https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html>`_.
        By default no arguments are passed. 
        Note that you should only pass in `region_name` or `aws_account_id` or other variables that will not effect credentials or credential refreshing. 

    Returns
    -------
    boto3.Session
        The assumed role session with automatic credential refreshing.

    Raises
    ------
    ForbiddenKWArgError
        One of the kwargs function parameters includes a keyword argument that is not allowed for boto3-assume.
    MissingKWArgError
        One of the kwargs function parameters is missing a necessary keyword argument.
    
    Examples
    --------
    A minimum example to assume a role:

    .. code-block:: python

        import boto3
        from boto3_assume import assume_role

        assume_session = assume_role(
            source_session=boto3.Session(), # You must pass in a boto3 session that automatically refreshes!
            assume_role_kwargs={
                "RoleArn": "arn:aws:iam::123412341234:role/my_role",
                "RoleSessionName": "my-role-session"
            }
        )
    """
    if "RoleArn" not in assume_role_kwargs or "RoleSessionName" not in assume_role_kwargs:
        raise MissingKWArgError("assume_role_kwargs must include the RoleArn and RoleSessionName keys.")

    if sts_client_kwargs is None:
        sts_client_kwargs = {}
    else:
        _check_forbidden_keys(
            name="sts_client_kwargs", 
            kwargs=sts_client_kwargs, 
            forbidden_keys=[
                "service_name",
                "aws_access_key_id",
                "aws_secret_access_key",
                "aws_session_token"
            ]
        )
    
    if target_session_kwargs is None:
        target_session_kwargs = {}
    else:
        _check_forbidden_keys(
            name="target_session_kwargs",
            kwargs=target_session_kwargs,
            forbidden_keys=[
                "aws_access_key_id",
                "aws_secret_access_key",
                "aws_session_token",
                "botocore_session",
                "profile_name"
            ]
        )
    
    assume_sess = boto3.Session(**target_session_kwargs)
    assume_sess._session._credentials = DeferredRefreshableCredentials(
        refresh_using=AssumeRefresh(
            source_session=source_session,
            sts_client_kwargs=sts_client_kwargs,
            assume_role_kwargs=assume_role_kwargs
        ).refresh,
        method="sts-assume-role"
    )
    
    return assume_sess
