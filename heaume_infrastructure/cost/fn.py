import pulumi
from pulumi_aws import iam, lambda_

from heaume_infrastructure.config import TAGS

role_lambda_retrieve_cost = iam.Role(
    "lambdaRetrieveCostRole",
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

role_policy_lambda_retrieve_cost = iam.RolePolicy(
    "lambdaRetrieveCostRolePolicy",
    role=role_lambda_retrieve_cost.id,
    policy="""{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": [
                "ce:GetCostAndUsage",
                "ce:GetDimensionValues",
                "ce:GetReservationUtilization",
                "ce:GetTags"
            ],
            "Resource": "*"
        },
        {
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

lambda_retrieve_cost = lambda_.Function(
    "lambdaRetrieveCost",
    role=role_lambda_retrieve_cost.arn,
    runtime="python3.7",
    handler="handler.handler",
    code=pulumi.AssetArchive(
        {".": pulumi.FileArchive("./heaume_infrastructure/cost/retrieve_cost")}
    ),
)
