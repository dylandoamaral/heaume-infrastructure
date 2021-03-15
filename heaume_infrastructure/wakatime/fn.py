import pulumi
from pulumi_aws import iam, lambda_

from heaume_infrastructure.config import TAGS
from heaume_infrastructure.utils.pulumi import config
from heaume_infrastructure.shared.layer import heaume_layer

wakatime_token = config.require_secret("wakatimeToken")

role_lambda_retrieve_wakatime = iam.Role(
    "lambdaRetrieveWakatimeRole",
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

role_policy_lambda_retrieve_wakatime = iam.RolePolicy(
    "lambdaRetrieveWakatimeRolePolicy",
    role=role_lambda_retrieve_wakatime.id,
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

lambda_retrieve_wakatime = lambda_.Function(
    "lambdaRetrieveWakatime",
    role=role_lambda_retrieve_wakatime.arn,
    runtime="python3.7",
    handler="handler.handler",
    code=pulumi.AssetArchive(
        {".": pulumi.FileArchive("./heaume_infrastructure/wakatime/retrieve_wakatime")}
    ),
    layers=[heaume_layer.arn],
    tags=TAGS,
    environment={"variables": {"token": wakatime_token}},
)
