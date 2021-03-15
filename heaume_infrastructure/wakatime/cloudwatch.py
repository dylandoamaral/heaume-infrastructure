import pulumi_aws as aws
from pulumi_aws import iam

from heaume_infrastructure.config import TAGS
from heaume_infrastructure.wakatime.sfn import sfn_handle_wakatime

role_event_handle_wakatime = iam.Role(
    "eventHandleWakatimeRole",
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
    tags=TAGS,
)

role_policy_event_handle_wakatime = iam.RolePolicy(
    "eventHandleWakatimeRolePolicy",
    role=role_event_handle_wakatime.id,
    policy=sfn_handle_wakatime.arn.apply(
        lambda arn: """{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "states:StartExecution"
                ],
                "Resource": "%s"
            }
        ]
    }"""
        % (arn)
    ),
)


handle_wakatime_cron = aws.cloudwatch.EventRule(
    "handleWakatimeCron",
    description="Launch Handle Wakatime Step Function each day",
    schedule_expression="cron(0 0 * * ? *)",
    tags=TAGS,
)

handle_wakatime_target = aws.cloudwatch.EventTarget(
    "handleWakatimeTarget",
    rule=handle_wakatime_cron.name,
    arn=sfn_handle_wakatime.arn,
    role_arn=role_event_handle_wakatime.arn,
)
