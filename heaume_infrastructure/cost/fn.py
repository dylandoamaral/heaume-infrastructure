import pulumi
from pulumi_aws import lambda_

from heaume_infrastructure.cost.iam import role_lambda_retrieve_cost

lambda_retrieve_cost = lambda_.Function(
    "lambdaRetrieveCost",
    role=role_lambda_retrieve_cost.arn,
    runtime="python3.7",
    handler="handler.handler",
    code=pulumi.AssetArchive(
        {".": pulumi.FileArchive("./heaume_infrastructure/cost/retrieve_cost")}
    ),
)
