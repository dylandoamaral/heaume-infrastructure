from pulumi import Output
from pulumi_aws import iam, sfn

from heaume_infrastructure.config import TAGS
from heaume_infrastructure.cost.fn import lambda_retrieve_cost
from heaume_infrastructure.shared.fn import lambda_write_to_influxdb
from heaume_infrastructure.utils.iam import policy_invoke_lambdas

sfn_lambda_arns = Output.all(lambda_retrieve_cost.arn, lambda_write_to_influxdb.arn)

role_sfn_handle_cost = iam.Role(
    "sfnHandleCostRole",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "states.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }""",
    tags=TAGS,
)

role_policy_sfn_handle_cost = iam.RolePolicy(
    "sfnHandleCostRolePolicy",
    role=role_sfn_handle_cost.id,
    policy=policy_invoke_lambdas(sfn_lambda_arns),
)

sfn_handle_cost = sfn.StateMachine(
    "sfnHandleCost",
    role_arn=role_sfn_handle_cost.arn,
    definition=sfn_lambda_arns.apply(
        lambda arns: """{
        "Comment": "Retrieve daily cost and send them to influxDB.",
        "StartAt": "RetrieveCost",
        "States": {
            "RetrieveCost": {
               "Type": "Task",
               "Resource": "%s",
               "Next": "WriteToInfluxDB"
            },
            "WriteToInfluxDB": {
                 "Type": "Task",
                 "Resource": "%s",
                 "End": true
            }
        }
    }"""
        % (arns[0], arns[1])
    ),
    tags=TAGS,
)
