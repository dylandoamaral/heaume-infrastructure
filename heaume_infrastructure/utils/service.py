from abc import ABC, abstractmethod


class Service(ABC):
    """A class describing AWS Service."""

    @abstractmethod
    def name(self) -> str:
        """Get the name of the service."""

    @abstractmethod
    def acronym(self) -> str:
        """Get the acronym of the service."""


class CostExplorer(Service):
    def name(self) -> str:
        return "Cost Explorer"

    def acronym(self) -> str:
        return "ce"


class CloudWatchLogs(Service):
    def name(self) -> str:
        return "CloudWatch Logs"

    def acronym(self) -> str:
        return "logs"


class CloudWatchEvents(Service):
    def name(self) -> str:
        return "CloudWatch Events"

    def acronym(self) -> str:
        return "events"


class Lambda(Service):
    def name(self) -> str:
        return "Lambda"

    def acronym(self) -> str:
        return "lambda"


class StepFunctions(Service):
    def name(self) -> str:
        return "Step Functions"

    def acronym(self) -> str:
        return "states"


no_resource_services = [CostExplorer()]
