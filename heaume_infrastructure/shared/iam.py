from pulumi_aws import iam

from heaume_infrastructure.config import tags

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
    tags=tags,
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
