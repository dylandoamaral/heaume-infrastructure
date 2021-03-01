import unittest

import pulumi

import heaume_infrastructure.shared.fn as infra
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


def describe_lambda_write_to_influxdb():
    def describe_role():
        def must_respect_assume_role_rules():
            check_assume_role_policy(role=infra.role_lambda_write_to_influxdb, service=Lambda())

    def describe_role_policy():
        def must_respect_policy_rules():
            check_policy(policy=infra.role_policy_lambda_write_to_influxdb)

        def must_give_access_to_cloudwatch_logs():
            check_policy_action(
                policy=infra.role_policy_lambda_write_to_influxdb, service=CloudWatchLogs()
            )

        def must_be_attached_to_role_lambda_write_to_influxdb():
            check_role_has_policy(
                role=infra.role_lambda_write_to_influxdb,
                policy=infra.role_policy_lambda_write_to_influxdb,
            )
