import pulumi
from pulumi_aws import lambda_, iam

from heaume_infrastructure.config import TAGS

from heaume_infrastructure.shared.layer import heaume_layer
from heaume_infrastructure.utils.pulumi import config

lambda_write_to_influxdb_url = config.require_secret("influxdbURL")
lambda_write_to_influxdb_token = config.require_secret("influxdbToken")

role_lambda_write_to_influxdb = iam.Role(
    "lambdaWriteToInfluxdbRole",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "sts:AssumeRole",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Effect": "Allow",
                "Sid": ""
            }
        ]
    }""",
    tags=TAGS,
)

role_policy_lambda_write_to_influxdb = iam.RolePolicy(
    "lambdaWriteToInfluxdbRolePolicy",
    role=role_lambda_write_to_influxdb.id,
    policy="""{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        }]
    }""",
)

lambda_write_to_influxdb = lambda_.Function(
    "lambdaWriteToInfluxdb",
    role=role_lambda_write_to_influxdb.arn,
    runtime="python3.7",
    handler="handler.handler",
    code=pulumi.AssetArchive(
        {".": pulumi.FileArchive("./heaume_infrastructure/shared/write_to_influxdb")}
    ),
    layers=[heaume_layer.arn],
    environment={
        "variables": {
            "url": lambda_write_to_influxdb_url,
            "token": lambda_write_to_influxdb_token,
        }
    },
)
