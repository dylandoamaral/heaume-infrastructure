import pulumi_aws as aws
from pulumi_aws import iam

from heaume_infrastructure.config import TAGS
from heaume_infrastructure.cost.iam import role_handle_cost_event
from heaume_infrastructure.cost.sfn import sfn_handle_cost

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
    tags=TAGS,
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


handle_cost_cron = aws.cloudwatch.EventRule(
    "handleCostCron",
    description="Launch Handle Cost Step Function each day",
    schedule_expression="cron(0 0 * * ? *)",
    tags=TAGS,
)

heandle_cost_target = aws.cloudwatch.EventTarget(
    "handleCostTarget",
    rule=handle_cost_cron.name,
    arn=sfn_handle_cost.arn,
    role_arn=role_handle_cost_event.arn,
)
