

from typing import Any, Dict

import aioboto3

from boto3_assume.assume_refresh import AssumeRefresh


class AIOAssumeRefresh(AssumeRefresh):

    def __init__(
        self, 
        source_session: aioboto3.Session,
        sts_client_kwargs: Dict[str, Any],
        assume_role_kwargs: Dict[str, Any]
    ):
        self._source_session = source_session
        self._sts_client_kwargs = sts_client_kwargs
        self._assume_role_kwargs = assume_role_kwargs


    async def refresh(self) -> Dict[str, Any]:
        # since this always needs to be a context manager we have to create the client every time
        async with self._source_session.client("sts", **self._sts_client_kwargs) as sts_client:
            response = await sts_client.assume_role(**self._assume_role_kwargs)
            creds = response['Credentials']
            return {
                'access_key': creds['AccessKeyId'],
                'secret_key': creds['SecretAccessKey'],
                'token': creds['SessionToken'],
                'expiry_time': self._serialize_if_needed(creds['Expiration']),
            }

