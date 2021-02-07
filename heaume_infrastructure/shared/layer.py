import pulumi
import pulumi_aws as aws

heaume_layer = aws.lambda_.LayerVersion(
    "heaumeLayer",
    layer_name="heaumeLayer",
    compatible_runtimes=["python3.8"],
    code=pulumi.FileArchive("heaume_infrastructure/shared/layer/heaume_layer.zip"),
)
