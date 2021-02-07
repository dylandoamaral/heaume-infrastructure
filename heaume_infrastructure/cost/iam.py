from pulumi_aws import config, iam

from heaume_infrastructure.config import tags

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
    tags=tags,
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

role_sfn_handle_cost = iam.Role(
    "sfnHandleCostRole",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "states.%s.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }"""
    % config.region,
    tags=tags,
)

role_policy_sfn_handle_cost = iam.RolePolicy(
    "sfnHandleCostRolePolicy",
    role=role_sfn_handle_cost.id,
    policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "lambda:InvokeFunction"
                ],
                "Resource": "*"
            }
        ]
    }""",
)

role_handle_cost_event = iam.Role(
    "eventHandleCostRole",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "events.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }""",
    tags=tags,
)

role_policy_handle_cost_event = iam.RolePolicy(
    "eventHandleCostRolePolicy",
    role=role_handle_cost_event.id,
    policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "states:StartExecution"
                ],
                "Resource": "*"
            }
        ]
    }""",
)
