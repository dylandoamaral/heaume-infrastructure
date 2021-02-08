import pulumi_aws as aws

from heaume_infrastructure.config import tags
from heaume_infrastructure.cost.iam import role_handle_cost_event
from heaume_infrastructure.cost.sfn import sfn_handle_cost

handle_cost_cron = aws.cloudwatch.EventRule(
    "handleCostCron",
    description="Launch Handle Cost Step Function each day",
    schedule_expression="cron(0 0 * * ? *)",
    tags=tags,
)

heandle_cost_target = aws.cloudwatch.EventTarget(
    "handleCostTarget",
    rule=handle_cost_cron.name,
    arn=sfn_handle_cost.arn,
    role_arn=role_handle_cost_event.arn,
)
