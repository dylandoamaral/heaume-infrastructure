import pulumi
from pulumi import ResourceOptions
from pulumi_aws import s3

from heaume_infrastructure.config import TAGS

bucket_heaume = s3.Bucket(
    "heaume",
    bucket="heaume",
    acl="private",
    tags=TAGS,
    opts=ResourceOptions(delete_before_replace=True, protect=True),
)
