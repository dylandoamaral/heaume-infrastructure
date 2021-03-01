import json
from typing import Optional

from pulumi_aws.iam import Role, RolePolicy

from heaume_infrastructure.utils.service import Service, no_resource_services
from tests.tools.pulumi import check_pulumi, check_pulumi_relationship


def check_policy(policy: RolePolicy):
    """
    Check if a policy respects the common assertion for all policies.

    :param policy: The policy to check.
    :type policy: RolePolicy
    """

    def curry(args):
        urn, policy = args
        policy = json.loads(policy)
        need = f"The policy {urn} should have"
        version_number = "2012-10-17"
        version = policy.get("Version")
        assert version, f"{need} a Version."
        assert version == version_number, f"{need} the {version_number}'s version."
        statement = policy.get("Statement")
        assert statement, f"{need} a Statement."
        assert isinstance(statement, list) is True, f"{need} a list for Statement."
        for index, statement in enumerate(policy["Statement"]):
            need = f"The policy {urn}'s Statement n°{index} should have"
            neednot = need.replace("have", "not have")
            assert isinstance(statement, dict), f"{need} a Statement of type dict."
            effect = statement.get("Effect")
            allowed_effects = ["Allow", "Deny"]
            str_effects = " or ".join(allowed_effects)
            assert effect, f"{need} an Effect."
            assert effect in allowed_effects, f"{need} an Effect equals to {str_effects}."
            resource = statement.get("Resource")
            assert resource, f"{need} a Resource."
            assert isinstance(resource, (str, list)), f"{need} a Resource of type list or str."
            actions = statement.get("Action")
            assert actions, f"{need} an Action."
            assert isinstance(actions, (str, list)), f"{need} an Action of type list or str."
            action_acronyms = {action.split(":")[0] for action in actions}
            no_ressources_acronyms = {s.acronym() for s in no_resource_services}
            if not all(s in no_ressources_acronyms for s in action_acronyms):
                assert resource != "*", f"{neednot} a wildcard Resource ('*')."

    check_pulumi(policy, "policy", curry)


def check_assume_role_policy(role: Role, service: Service):
    """
    Check if an assume role respects the common assertion for all assume roles.

    :param role: The role that need to be assumed.
    :type role: Role
    :param service: The name of the service that assume the role.
    :type service: Service
    """

    def curry(args):
        urn, policy = args
        policy = json.loads(policy)
        need = f"The assume policy {urn} should have"
        version_number = "2012-10-17"
        version = policy.get("Version")
        assert version, f"{need} a Version."
        assert version == version_number, f"{need} the {version_number}'s Version."
        statements = policy.get("Statement")
        assert statements, f"{need} a Statement."
        assert isinstance(statements, list) is True, f"{need} a list for Statement."
        assert len(statements) == 1, f"{need} only one Statement."
        statement = statements[0]
        need = f"The statement of {urn} should have"
        need_be = need.replace("have", "be")
        assert statement["Action"] == "sts:AssumeRole", f"{need_be} 'sts:AssumeRole'."
        principal = statement.get("Principal")
        assert principal, f"{need} a Principal."
        assert isinstance(principal, dict), f"{need} a Principal of type dict."
        service_ = principal.get("Service")
        assert service_, f"{need} a principal's Service."
        assert service_.startswith(service.acronym()), f"{need} to be assign to a {service.name()}."
        effect = statement.get("Effect")
        assert effect, f"{need} an Effect."
        assert effect == "Allow", f"{need} an Effect equals to Allow."

    check_pulumi(role, "assume_role_policy", curry)


def check_policy_action(policy: RolePolicy, service: Service, category: Optional[str] = None):
    """
    Check if a policy allowed at least one action for a particular service.

    .. info::

       The policy should be asserted using `check_policy` first.

    :param policy: The policy to check.
    :type policy: RolePolicy
    :param service: The name of the service.
    :type service: Service
    :param category: The category of the action that need to be authorized,
                     defaults to None.
    :type category: str, optional
    """

    def curry(args):
        urn, policy = args
        policy = json.loads(policy)
        statement = policy["Statement"]
        need = f"The policy {urn} should have"
        acronym = f"{service.acronym()}:{category}" if category else service.acronym()
        for statement in policy["Statement"]:
            actions = statement["Action"]
            actions = actions if isinstance(actions, list) else [actions]
            effect = statement["Effect"]
            for action in actions:
                if action.startswith(acronym) and effect == "Allow":
                    return
        assert False, f"{need} an allowed action for the service {service.name()}."

    check_pulumi(policy, "policy", curry)


def check_role_has_policy(role: Role, policy: RolePolicy):
    """
     heck if a policy is attached to a role.

    :param role: The role.
    :type role: Role
    :param policy: The policy.
    :type policy: RolePolicy
    """
    check_pulumi_relationship(policy, "role", role, "id")
