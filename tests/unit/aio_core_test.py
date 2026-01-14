
import time
import datetime

import aioboto3
from botocore.config import Config
import pytest
import pytz

from boto3_assume import assume_role_aio_session
from boto3_assume.aio_assume_refresh import AIOAssumeRefresh


@pytest.mark.asyncio
async def test_assume_role_no_extra_kwargs(
    moto_server: str,
    role_arn: str,
    session_name: str
) -> None:
    sess = aioboto3.Session()
    with pytest.deprecated_call():
        assume_sess = assume_role_aio_session(
            source_session=sess,
            RoleArn=role_arn,
            RoleSessionName=session_name
        )
    assert assume_sess._session._credentials._refresh_using.__self__._sts_client_kwargs == {}
    assert assume_sess._session._credentials._refresh_using.__self__._assume_role_kwargs == {
        "RoleArn": role_arn, 
        "RoleSessionName": session_name
    }
    

@pytest.mark.asyncio
async def test_assume_role(
    moto_server: str,
    role_arn: str,
    session_name: str,
    sts_arn: str
) -> None:
    sess = aioboto3.Session()
    with pytest.deprecated_call():
        assume_sess = assume_role_aio_session(
            source_session=sess,
            RoleArn=role_arn,
            RoleSessionName=session_name,
            sts_client_kwargs={
                "endpoint_url": moto_server,
                "region_name": "us-east-1"
            }
        )
    # credentials should only be retrieved once an API call is made
    creds = await assume_sess.get_credentials()
    assert creds._expiry_time == None
    async with assume_sess.client("sts", endpoint_url=moto_server, region_name="us-east-1") as sts_client:
        identity = await sts_client.get_caller_identity()
        creds = await assume_sess.get_credentials()
        assert identity['Arn'] == sts_arn
        assert creds._expiry_time != None
        assert isinstance(creds._refresh_using.__self__, AIOAssumeRefresh)
        assert creds._refresh_using.__self__._source_session == sess
        assert creds._refresh_using.__self__._sts_client_kwargs == {
            "endpoint_url": "http://localhost:5000", 
            "region_name": "us-east-1"
        }
        assert creds._refresh_using.__self__._assume_role_kwargs == {
            "RoleArn": role_arn, 
            "RoleSessionName": session_name
        }
        

@pytest.mark.asyncio
async def test_assume_role_extra_kwargs(
    moto_server: str,
    role_arn: str,
    session_name: str
) -> None:
    sess = aioboto3.Session()
    boto_config = Config(
        retries={
            "total_max_attempts": 10,
            "mode": "adaptive"
        }
    )
    with pytest.deprecated_call():
        assume_sess = assume_role_aio_session(
            source_session=sess,
            RoleArn=role_arn,
            RoleSessionName=session_name,
            sts_client_kwargs={
                "endpoint_url": moto_server,
                "region_name": "us-east-1",
                "config": boto_config
            },
            assume_role_kwargs={
                "DurationSeconds": 900
            }
        )
    async with assume_sess.client("sts", region_name="us-east-1", endpoint_url=moto_server)as sts_client:
        await sts_client.get_caller_identity()
        creds = await assume_sess.get_credentials()
        expires_at: datetime.datetime = creds._expiry_time.astimezone(pytz.UTC).replace(tzinfo=None)
        until_expire = - (datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) - expires_at)
        # test to make sure that the variables were passed so the duration should be 900
        assert until_expire.total_seconds() < 900
        assert until_expire.total_seconds() > 880

        assert creds._refresh_using.__self__._source_session == sess
        assert creds._refresh_using.__self__._sts_client_kwargs == {
            "endpoint_url": "http://localhost:5000", 
            "region_name": "us-east-1",
            "config": boto_config
        }
        assert creds._refresh_using.__self__._assume_role_kwargs == {
            "RoleArn": role_arn, 
            "RoleSessionName": session_name,
            "DurationSeconds": 900
        }
        

@pytest.mark.asyncio
async def test_refresh_creds(
    moto_server: str,
    role_arn: str,
    session_name: str,
    sts_arn: str
) -> None:
    sess = aioboto3.Session()
    with pytest.deprecated_call():
        assume_sess = assume_role_aio_session(
            source_session=sess,
            RoleArn=role_arn,
            RoleSessionName=session_name,
            sts_client_kwargs={
                "endpoint_url": moto_server,
                "region_name": "us-east-1"
            },
            assume_role_kwargs={
                "DurationSeconds": 900
            }
        )
    async with assume_sess.client("sts", endpoint_url=moto_server, region_name="us-east-1") as sts_client:
        identity = await sts_client.get_caller_identity()
        assert identity['Arn'] == sts_arn
        # save the original expire ~ 900 seconds from now
        original_expire = assume_sess._session._credentials._expiry_time
        # create a new one that expires now
        assume_sess._session._credentials._expiry_time = pytz.UTC.localize(datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None))
        assert assume_sess._session._credentials._expiry_time < original_expire
        # then sleep so there is a difference
        time.sleep(2)
        # call again so creds refresh
        identity = await sts_client.get_caller_identity()
        assert identity['Arn'] == sts_arn
        # the new expire time should be slightly more than the original !2 seconds
        assert assume_sess._session._credentials._expiry_time > original_expire
    

    


