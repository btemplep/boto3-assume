

import datetime
from typing import Any, Dict

import boto3


class AssumeRefresh:

    def __init__(
        self, 
        source_session: boto3.Session,
        sts_client_kwargs: Dict[str, Any],
        assume_role_kwargs: Dict[str, Any]
    ):
        self._source_session = source_session
        self._sts_client_kwargs = sts_client_kwargs
        self._assume_role_kwargs = assume_role_kwargs
        self._sts_client = self._source_session.client("sts", **self._sts_client_kwargs)
    

    def _serialize_if_needed(self, value):
        if isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%dT%H:%M:%S%Z')

        return value


    def refresh(self) -> Dict[str, Any]:
        creds = self._sts_client.assume_role(**self._assume_role_kwargs)['Credentials']

        return {
            'access_key': creds['AccessKeyId'],
            'secret_key': creds['SecretAccessKey'],
            'token': creds['SessionToken'],
            'expiry_time': self._serialize_if_needed(creds['Expiration']),
        }

