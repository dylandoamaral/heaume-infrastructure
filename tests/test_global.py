# import pulumi
# import pytest
# from pulumi import CustomResource, Output
# import heaume_infrastructure.cost.cloudwatch as infra
# from heaume_infrastructure.config import TAGS


# https://github.com/pulumi/pulumi/issues/6439
# def describe_tags():
#     names = [item for item in dir(infra) if not item.startswith("__")]
#     variables = [getattr(infra, name) for name in names]
#     resources = [variable for variable in variables if isinstance(variable, CustomResource)]
#     tupled = [(resource) for resource in resources]

#     @pulumi.runtime.test
#     @pytest.mark.parametrize("resource", tupled)
#     def must_be_setup(resource):
#         def assertion(args):
#             urn, tags = args
#             assert tags == TAGS, f"The resource {urn} should have tags."

#         try:
#             return Output.all(resource.urn, resource.tags).apply(assertion)
#         except AttributeError:
#             return True
