# boto3-assume


`boto3-assume` has one simple goal. Easily create `boto3`/`aioboto3` assume role sessions with automatic credential refreshing.


## Installation

Install with pip:

```text
$ pip install boto3-assume
```

It doesn't come with `boto3` or `aioboto3` by default, 
but if you want to install them with the package it can be done as extras.

```text
$ pip install boto3-assume[aioboto,boto3]
```


## Tutorial

There are only 2 functions `assume_role_session` and `assume_role_aio_session`

For boto3:

```python
import boto3
from boto3_assume import assume_role_session

assume_session = assume_role_session(
    source_session=boto3.Session(), # You must pass in a boto3 session that automatically refreshes!
    RoleArn="arn:aws:iam::123412341234:role/my_role",
    RoleSessionName="my-role-session"
)

# use the assumed session!
sts_client = assume_session.client("sts", region_name="us-east-1")
print(sts_client.get_caller_identity())
# {
#     "UserId": "EXAMPLEID", 
#     "Account": "123412341234", 
#     "Arn": "arn:aws:sts::123412341234:role/my_role", 
#     "ResponseMetadata": {
#         "RequestId": "asdfqwfqwfasdfasdfasfsdf", 
#         "HTTPStatusCode": 200, 
#         "HTTPHeaders": {
#             "server": "amazon.com", 
#             "date": "Tue, 27 Jun 2023 00:00:00 GMT"
#         }, 
#         "RetryAttempts": 0
#     }
# }
```

For `aioboto3`:

```python
import asyncio

import aioboto3
from boto3_assume import assume_role_aio_session

# since this uses "Deferred" credentials you don't need to call this within a coroutine or context manager
assume_session = assume_role_session(
    source_session=aioboto3.Session(), # You must pass in an aioboto3 session that automatically refreshes!
    RoleArn="arn:aws:iam::123412341234:role/my_role",
    RoleSessionName="my-role-session"
)

async def main():
    # use the assumed session!
    async with assume_session.client("sts", region_name="us-east-1") as sts_client:
        print(await sts_client.get_caller_identity())
        # {
        #     "UserId": "EXAMPLEID", 
        #     "Account": "123412341234", 
        #     "Arn": "arn:aws:sts::123412341234:role/my_role", 
        #     "ResponseMetadata": {
        #         "RequestId": "asdfqwfqwfasdfasdfasfsdf", 
        #         "HTTPStatusCode": 200, 
        #         "HTTPHeaders": {
        #             "server": "amazon.com", 
        #             "date": "Tue, 27 Jun 2023 00:00:00 GMT"
        #         }, 
        #         "RetryAttempts": 0
        #     }
        # }

asyncio.run(main())
```

Under the hood a `boto3`/`aioboto3` sts client will be created and `assume_role` called to get/refresh credentials.

If you want you can also specify extra kwargs for the [sts client](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.client), and for the [assume_role](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/assume_role.html) call.


> **NOTE**: The `"sts"` service is already specified for the client. 
`RoleArn` and `RoleSessionName` are used in the assume role call. 

```python
import boto3
from boto3_assume import assume_role_session
from botocore.config import Config

assume_session = assume_role_session(
    source_session=boto3.Session(), # You must pass in a boto3 session that automatically refreshes!
    RoleArn="arn:aws:iam::123412341234:role/my_role",
    RoleSessionName="my-role-session",
    sts_client_kwargs={
        "region_name": "us-east-1",
        "config": Config(
            retries={
                "total_max_attempts": 10,
                "mode": "adaptive"
            }
        )
    },
    assume_role_kwargs={
        "DurationSeconds": 900
    }
)
```

## Development

Install the package in editable mode with dev dependencies.

```text
(venv) $ pip install -e .[dev,all]
```

[nox](https://nox.thea.codes/en/stable/) is used to manage various dev functions.
Start with

```text
(venv) $ nox --help
```

[pyenv](https://github.com/pyenv/pyenv) is used to manage python versions. 
To run the nox tests for applicable python version you will first need to install them. 
In the root project dir run:

```text
(venv) $ pyenv install
```
