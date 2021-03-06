from pulumi import Output
from pulumi_aws import iam, sfn

from heaume_infrastructure.config import TAGS
from heaume_infrastructure.shared.fn import lambda_write_to_influxdb
from heaume_infrastructure.utils.iam import policy_invoke_lambdas
from heaume_infrastructure.wakatime.fn import lambda_retrieve_wakatime

sfn_lambda_arns = Output.all(lambda_retrieve_wakatime.arn, lambda_write_to_influxdb.arn)

role_sfn_handle_wakatime = iam.Role(
    "sfnHandleWakatimeRole",
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

role_policy_sfn_handle_wakatime = iam.RolePolicy(
    "sfnHandleWakatimeRolePolicy",
    role=role_sfn_handle_wakatime.id,
    policy=policy_invoke_lambdas(sfn_lambda_arns),
)

sfn_handle_wakatime = sfn.StateMachine(
    "sfnHandleWakatime",
    role_arn=role_sfn_handle_wakatime.arn,
    definition=sfn_lambda_arns.apply(
        lambda arns: """{
        "Comment": "Retrieve daily wakatime wakatime and send them to influxDB.",
        "StartAt": "RetrieveWakatime",
        "States": {
            "RetrieveWakatime": {
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
