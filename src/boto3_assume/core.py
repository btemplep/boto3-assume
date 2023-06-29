
from typing import Any, Dict, Optional

import boto3
from botocore.credentials import DeferredRefreshableCredentials

from boto3_assume.assume_refresh import AssumeRefresh


def assume_role_session(
    source_session: boto3.Session,
    RoleArn: str, 
    RoleSessionName: str, 
    sts_client_kwargs: Optional[Dict[str, Any]] = None,
    assume_role_kwargs: Optional[Dict[str, Any]] = None
) -> boto3.Session:
    """Generate an assume role ``boto3`` session, that will automatically refresh credentials.

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
