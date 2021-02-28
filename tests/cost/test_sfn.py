import pulumi
from tests.tools.iam import (
    check_policy,
    check_assume_role_policy,
    check_policy_action,
    check_role_has_policy,
)
import unittest

from heaume_infrastructure.utils.service import CostExplorer, CloudWatchLogs, Lambda, StepFunctions

import heaume_infrastructure.cost.sfn as infra  # noqa


def describe_role_sfn_handle_cost():
    def must_respect_assume_role_rules():
        check_assume_role_policy(role=infra.role_sfn_handle_cost, service=StepFunctions())


def describe_role_policy_sfn_handle_cost():
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
