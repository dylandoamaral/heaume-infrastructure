import pulumi
from pulumi import CustomResource

from typing import Any, Callable

from heaume_infrastructure.utils.service import Service


@pulumi.runtime.test
def check_pulumi(resource: CustomResource, attribute: Any, function: Callable[[str, str], None]):
    """Check a pulumi resource's attribute using a function that takes two parameters,
    the urn of the resource and the attribute to evaluate.

    :param resource: The resource to evaluate.
    :type resource: CustomResource
    :param attribute: The attribute of the resource.
    :type attribute: Any
    :param function: The function to evaluate the attribue.
    :type function: Callable[[str, str], None]
    """
    urn = resource.urn
    anything = getattr(resource, attribute)
    return pulumi.Output.all(urn, anything).apply(function)


@pulumi.runtime.test
def check_pulumi_relationship(
    left_resource: CustomResource,
    left_attribute: Any,
    right_resource: CustomResource,
    right_attribute: Any,
):
    def curry(args):
        left, right = args
        assert left == right, f"{left} not equals to {right}."

    left = getattr(left_resource, left_attribute)
    right = getattr(right_resource, right_attribute)
    return pulumi.Output.all(left, right).apply(curry)
