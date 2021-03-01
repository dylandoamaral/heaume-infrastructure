import unittest

import pulumi
from pulumi import CustomResource

import heaume_infrastructure.cost.cloudwatch as infra
from heaume_infrastructure.utils.service import CloudWatchEvents, StepFunctions
from tests.tools.iam import (
    check_assume_role_policy,
    check_policy,
    check_policy_action,
    check_role_has_policy,
)


def describe_event_handle_cost():
    def describe_role():
        def must_respect_assume_role_rules():
            check_assume_role_policy(role=infra.role_event_handle_cost, service=CloudWatchEvents())

    def describe_role_policy():
        def must_respect_policy_rules():
            check_policy(policy=infra.role_policy_event_handle_cost)

        def must_give_access_to_step_functions():
            check_policy_action(policy=infra.role_policy_event_handle_cost, service=StepFunctions())

        def must_be_attached_to_role_event_handle_cost():
            check_role_has_policy(
                role=infra.role_event_handle_cost, policy=infra.role_policy_event_handle_cost
            )
