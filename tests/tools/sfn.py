import json

from pulumi_aws.sfn import StateMachine

from heaume_infrastructure.utils.service import Service, no_resource_services
from tests.tools.pulumi import check_pulumi, check_pulumi_relationship


def check_asl(states: StateMachine):
    """
    Check if a step functions asl respects the common assertion for all step functions.

    :param states: The state machine.
    :type states: StateMachine
    """

    def curry(args):
        urn, asl = args
        asl = json.loads(asl)
        need = f"The states {urn} should have"
        start = asl.get("StartAt")
        assert start, f"{need} a StartAt."
        states = asl.get("States")
        end = False
        state_keys = states.keys()
        assert start in state_keys, f"{need} a StartAt refering to a task  but {start}."
        for index, (name, task) in enumerate(states.items()):
            type_ = task.get("Type")
            types = ["Task"]
            type_names = ", ".join(types)
            should = f"The task {index} of {urn} should have"
            assert type_, f"{should} a Type"
            assert type_ in types, f"{should} have a Type in {type_names}."
            if task.get("End") == True:
                if not end:
                    end = True
                else:
                    raise AssertionError(f"{need} only one end.")
            elif task.get("Next"):
                next_ = task.get("Next")
                assert next_, f"{should} a Next"
                assert next_ in state_keys, f"{should} a Next refering to another task but {next_}."
            else:
                then_keys = ", ".join(["End", "Next"])
                raise AssertionError(f"{should} at least one of the following keys: {then_keys}")
        if not end:
            raise AssertionError(f"{need} an end.")

    check_pulumi(states, "definition", curry)
