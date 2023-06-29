

import asyncio
import atexit
from contextlib import AsyncExitStack
import time

import aioboto3
import boto3

import boto3_assume

boto3_assume.assume_role_session(
    source_session=boto3.Session(),
    RoleArn="arn:aws:iam::123412341234:role/my_role",
    RoleSessionName="my-role-session"
)

# sts_client = boto3.client("sts", region_name="us-east-1")
# print(sts_client.get_caller_identity())
# assume_sess = assume_role(sts_client=sts_client, RoleArn="arn:aws:iam::174866956505:role/first-ec2-role", RoleSessionName="my-tester")
# assume_sts_client = assume_sess.client("sts", region_name="us-east-1")

# print(assume_sts_client.get_caller_identity())

# def close_stack(stack):
#     try:
#         loop = asyncio.get_running_loop()
#     except RuntimeError:
#         loop = asyncio.new_event_loop()

#     if loop.is_running() is True:
#         loop.create_task(asyncio.Task(aclose_stack(stack)))
#     else:
#         loop.run_until_complete(aclose_stack(stack))


# async def aclose_stack(stack):
#     await stack.aclose()
#     await stack.aclose()

sess = aioboto3.Session()

from botocore.config import Config

boto_config = Config(
    retries={
        "total_max_attempts": 10,
        "mode": "adaptive"
    }
)

assume_sess = boto3_assume.assume_role_aio_session(
    source_session=sess,
    RoleArn="arn:aws:iam::174866956505:role/first-ec2-role",
    RoleSessionName="tester",
    sts_client_kwargs={
        "region_name": "us-east-1",
        "config": boto_config
    },
    assume_role_kwargs={
        "DurationSeconds": 900
    }
)

async def main():
    async with assume_sess.client("sts", region_name="us-east-2") as sts_client:
        print(sts_client.meta.config.__dict__)
        print(await sts_client.get_caller_identity())
        print("sleeping for 15 mintutes")
        # await asyncio.sleep(915)
        # print("Should refresh creds")
        # print(await sts_client.get_caller_identity())

    
asyncio.run(main())
