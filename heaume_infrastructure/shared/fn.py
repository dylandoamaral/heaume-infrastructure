import pulumi
from pulumi_aws import lambda_

from heaume_infrastructure.shared.iam import role_lambda_write_to_influxdb
from heaume_infrastructure.shared.layer import heaume_layer
from heaume_infrastructure.utils.pulumi import config

lambda_write_to_influxdb_url = config.require_secret("influxdbURL")
lambda_write_to_influxdb_token = config.require_secret("influxdbToken")

lambda_write_to_influxdb = lambda_.Function(
    "lambdaWriteToInfluxdb",
    role=role_lambda_write_to_influxdb.arn,
    runtime="python3.7",
    handler="handler.handler",
    code=pulumi.AssetArchive(
        {".": pulumi.FileArchive("./heaume_infrastructure/shared/write_to_influxdb")}
    ),
    layers=[heaume_layer.arn],
    environment={
        "variables": {
            "url": lambda_write_to_influxdb_url,
            "token": lambda_write_to_influxdb_token,
        }
    },
)
