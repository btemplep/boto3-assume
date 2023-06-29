
from typing import Any, Dict, Optional

import aioboto3
from aiobotocore.credentials import AioDeferredRefreshableCredentials

from boto3_assume.aio_assume_refresh import AIOAssumeRefresh


def assume_role_aio_session(
    source_session: aioboto3.Session,
    RoleArn: str, 
    RoleSessionName: str, 
    sts_client_kwargs: Optional[Dict[str, Any]] = None,
    assume_role_kwargs: Optional[Dict[str, Any]] = None
) -> aioboto3.Session:
    """Generate an assume role ``aioboto3`` session, that will automatically refresh credentials.

    Parameters
    ----------
    source_session : aioboto3.Session
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
    aioboto3.Session
        The assumed role session.
    """
    if sts_client_kwargs is None:
        sts_client_kwargs = {}
    
    if assume_role_kwargs is None:
        assume_role_kwargs = {}

    assume_role_kwargs['RoleArn'] = RoleArn
    assume_role_kwargs['RoleSessionName'] = RoleSessionName
    assume_sess = aioboto3.Session()
    assume_sess._session._credentials = AioDeferredRefreshableCredentials(
        refresh_using=AIOAssumeRefresh(
            source_session=source_session,
            sts_client_kwargs=sts_client_kwargs,
            assume_role_kwargs=assume_role_kwargs
        ).refresh,
        method="sts-assume-role"
    )
    
    return assume_sess
