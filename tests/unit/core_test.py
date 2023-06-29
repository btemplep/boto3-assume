
import datetime
import time

import boto3
from botocore.config import Config
import pytz

from boto3_assume import assume_role_session
from boto3_assume.assume_refresh import AssumeRefresh


def test_assume_role(
    sts_moto: None,
    role_arn: str,
    session_name: str,
    sts_arn: str
) -> None:
    sess = boto3.Session()
    assume_sess = assume_role_session(
        source_session=sess,
        RoleArn=role_arn,
        RoleSessionName=session_name
    )
    # credentials should only be retrieved once an API call is made
    assert assume_sess.get_credentials()._expiry_time == None
    sts_client = assume_sess.client("sts")
    identity = sts_client.get_caller_identity()
    creds = assume_sess.get_credentials()
    assert identity['Arn'] == sts_arn
    assert creds._expiry_time != None
    assert isinstance(creds._refresh_using.__self__, AssumeRefresh)
    assert creds._refresh_using.__self__._source_session == sess
    assert creds._refresh_using.__self__._sts_client_kwargs == {}
    assert creds._refresh_using.__self__._assume_role_kwargs == {
        "RoleArn": role_arn, 
        "RoleSessionName": session_name
    }
    

def test_assume_role_extra_kwargs(
    sts_moto: None,
    role_arn: str,
    session_name: str
) -> None:
    sess = boto3.Session()
    boto_config = Config(
        retries={
            "total_max_attempts": 10,
            "mode": "adaptive"
        }
    )
    assume_sess = assume_role_session(
        source_session=sess,
        RoleArn=role_arn,
        RoleSessionName=session_name,
        sts_client_kwargs={
            "region_name": "us-east-1",
            "config": boto_config
        },
        assume_role_kwargs={
            "DurationSeconds": 900
        }
    )
    sts_client = assume_sess.client("sts")
    sts_client.get_caller_identity()
    creds = assume_sess.get_credentials()
    expires_at: datetime.datetime = creds._expiry_time.astimezone(pytz.UTC).replace(tzinfo=None)
    until_expire = - (datetime.datetime.utcnow() - expires_at)
    # test to make sure that the variables were passed so the duration should be 900
    assert until_expire.total_seconds() < 900
    assert until_expire.total_seconds() > 880

    assert creds._refresh_using.__self__._source_session == sess
    assert creds._refresh_using.__self__._sts_client_kwargs == {
        "region_name": "us-east-1",
        "config": boto_config
    }
    assert creds._refresh_using.__self__._assume_role_kwargs == {
        "RoleArn": role_arn, 
        "RoleSessionName": session_name,
        "DurationSeconds": 900
    }
    assert creds._refresh_using.__self__._sts_client.meta.config.region_name == "us-east-1"
    assert creds._refresh_using.__self__._sts_client.meta.config.retries['mode'] == "adaptive"
    assert creds._refresh_using.__self__._sts_client.meta.config.retries['total_max_attempts'] == 10
    


def test_refresh_creds(
    sts_moto: None,
    role_arn: str,
    session_name: str,
    sts_arn: str
) -> None:
    sess = boto3.Session()
    assume_sess = assume_role_session(
        source_session=sess,
        RoleArn=role_arn,
        RoleSessionName=session_name,
        assume_role_kwargs={
            "DurationSeconds": 900
        }
    )
    sts_client = assume_sess.client("sts")
    identity = sts_client.get_caller_identity()
    assert identity['Arn'] == sts_arn
    # save the original expire ~ 900 seconds from now
    original_expire = assume_sess._session._credentials._expiry_time
    # create a new one that expires now
    assume_sess._session._credentials._expiry_time = pytz.UTC.localize(datetime.datetime.utcnow())
    assert assume_sess._session._credentials._expiry_time < original_expire
    # then sleep so there is a difference
    time.sleep(2)
    # call again so creds refresh
    identity = sts_client.get_caller_identity()
    # the new expire time should be slightly more than the original !2 seconds
    assert assume_sess._session._credentials._expiry_time > original_expire
    

def test__serialize_if_needed() -> None:
    refresh = AssumeRefresh(
        source_session=boto3.Session(),
        sts_client_kwargs={},
        assume_role_kwargs={}
    )
    dt_str = "2023-06-27T00:00:00"
    result = refresh._serialize_if_needed(dt_str)
    assert result == dt_str

    
    


