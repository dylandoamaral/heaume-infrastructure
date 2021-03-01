import unittest

import pulumi

import heaume_infrastructure.cost.sfn as infra  # noqa
from heaume_infrastructure.utils.service import (
    CloudWatchLogs,
    CostExplorer,
    Lambda,
    StepFunctions,
)
from tests.tools.iam import (
    check_assume_role_policy,
    check_policy,
    check_policy_action,
    check_role_has_policy,
)
from tests.tools.sfn import check_asl


def describe_step_function_handle_cost():
    def describe_role():
        def must_respect_assume_role_rules():
            check_assume_role_policy(role=infra.role_sfn_handle_cost, service=StepFunctions())

    def describe_role_policy():
        def must_respect_policy_rules():
            check_policy(policy=infra.role_policy_sfn_handle_cost)

        def must_give_access_to_lambda_invocation():
            policy = infra.role_policy_sfn_handle_cost
            check_policy_action(
                policy=infra.role_policy_sfn_handle_cost,
                service=Lambda(),
                category="InvokeFunction",
            )

        def must_be_attached_to_role_sfn_handle_cost():
            check_role_has_policy(
                role=infra.role_sfn_handle_cost, policy=infra.role_policy_sfn_handle_cost
            )

    def describe_asl():
        def must_respect_asl_rules():
            check_asl(states=infra.sfn_handle_cost)