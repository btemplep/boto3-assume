# boto3-assume


Easily create `boto3` assume role sessions with automatic credential refreshing.

> **NOTE** - For `aioboto3` support, see [aioboto3-assume](https://pypi.org/project/aioboto3-assume/).


## Installation

Install with pip:

```text
$ pip install boto3-assume
```

## Tutorial

A minimal example: 

```python
import boto3
from boto3_assume import assume_role

assume_session = assume_role(
    source_session=boto3.Session(), # You must pass in a boto3 session that automatically refreshes!
    assume_role_kwargs={
        "RoleArn": "arn:aws:iam::123412341234:role/my_role",
        "RoleSessionName": "my-role-session"
    }
)

# Create clients, and their credentials will auto-refresh when expired!
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

Under the hood a `boto3` sts client will be created and `assume_role` called to get/refresh credentials.

You can pass the kwargs parameters as so:
- `assume_role_kwargs` - Keyword arguments to pass when calling [assume_role](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts/client/assume_role.html) with a boto3 STS client. 
    - Must at least provide `RoleArn` and `RoleSessionName` as outlined in the boto3 docs.
- `sts_client_kwargs` - Kwargs to pass when creating the [boto3 low level client](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.client) for [STS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html)
    - By default only the service argument will be passed as ``"sts"``. 
    - Note that you should not pass in the ``service_name`` or credentials here. 
- `target_session_kwargs` - Keyword arguments to pass when creating a the new target [boto3 Session](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html)
    - By default no arguments are passed. 
    - Note that you should only pass in `region_name` or `aws_account_id` or other variables that will not effect credentials or credential refreshing. 

A more complex example:

```python
import boto3
from boto3_assume import assume_role
from botocore.config import Config

assume_session = assume_role(
    source_session=boto3.Session(), 
    assume_role_kwargs={
        "RoleArn": "arn:aws:iam::123412341234:role/my_role",
        "RoleSessionName": "my-role-session",
        "DurationSeconds": 900,
        "Tags": [
            {
                "Key": "MyKey",
                "Value": "MyValue"
            }
        ]
    },
    sts_client_kwargs={
        "config": Config(
            retries={
                "total_max_attempts": 10,
                "mode": "adaptive"
            }
        )
    },
    target_session_kwargs={
        "region_name": "us-east-1"
    }
)
```

## Development

Install the package in editable mode with dev dependencies.

```text
(venv) $ pip install -e .[dev]
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
