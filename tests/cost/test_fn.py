import pulumi
from tests.tools.iam import (
    check_policy,
    check_assume_role_policy,
    check_policy_action,
    check_role_has_policy,
)
import unittest

from heaume_infrastructure.utils.service import CostExplorer, CloudWatchLogs, Lambda, StepFunctions

import heaume_infrastructure.cost.fn as infra


def describe_role_of_lambda_retrieve_cost():
    def must_respect_assume_role_rules():
        check_assume_role_policy(role=infra.role_lambda_retrieve_cost, service=Lambda())


def describe_role_policy_of_lambda_retrieve_cost():
    def must_respect_policy_rules():
        check_policy(policy=infra.role_policy_lambda_retrieve_cost)

    def must_give_access_to_cost_explorer():
        check_policy_action(policy=infra.role_policy_lambda_retrieve_cost, service=CostExplorer())

    def must_give_access_to_cloudwatch_logs():
        check_policy_action(policy=infra.role_policy_lambda_retrieve_cost, service=CloudWatchLogs())

    def must_be_attached_to_role_lambda_retrieve_cost():
        check_role_has_policy(
            role=infra.role_lambda_retrieve_cost, policy=infra.role_policy_lambda_retrieve_cost
        )
