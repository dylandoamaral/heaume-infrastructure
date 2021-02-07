from pulumi import Output
from pulumi_aws import sfn

from heaume_infrastructure.cost.fn import lambda_retrieve_cost
from heaume_infrastructure.cost.iam import role_sfn_handle_cost
from heaume_infrastructure.shared.fn import lambda_write_to_influxdb

sfn_lambdas = Output.all(lambda_retrieve_cost.arn, lambda_write_to_influxdb.arn)

sfn_handle_cost = sfn.StateMachine(
    "sfnHandleCost",
    role_arn=role_sfn_handle_cost.arn,
    definition=sfn_lambdas.apply(
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
)
