import pulumi

from heaume_infrastructure.shared.s3 import bucket_heaume
from tests.tools.pulumi import check_pulumi


def describe_heaume_bucket():
    def it_must_be_named_heaume():
        def curry(args):
            urn, bucket = args
            assert bucket == "heaume", "The bucket 'heaume' should be named heaume."

        check_pulumi(bucket_heaume, "bucket", curry)

    def it_must_be_private():
        def curry(args):
            urn, acl = args
            assert acl == "private", "The bucket 'heaume' should be private."

        check_pulumi(bucket_heaume, "acl", curry)
