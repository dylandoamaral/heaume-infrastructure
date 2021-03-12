import pulumi
import pytest
import pkgutil
from pulumi import CustomResource, Output
import heaume_infrastructure
from heaume_infrastructure.config import TAGS
from tests.tools.pulumi import check_pulumi


def describe_tags():
    package = heaume_infrastructure.__path__
    prefix = heaume_infrastructure.__name__ + "."
    modules = [
        importer.find_module(modname).load_module(modname)
        for importer, modname, _ in pkgutil.walk_packages(package, prefix)
    ]
    resources = sorted(
        {
            (item, getattr(module, item))
            for module in modules
            for item in dir(module)
            if not item.startswith("__")
            if isinstance(getattr(module, item), CustomResource)
        },
        key=lambda tuple: tuple[0],
    )

    @pytest.mark.parametrize("name,resource", resources)
    def must_be_setup(resource, name):
        def curry(args):
            urn, tags = args
            assert tags == TAGS, f"The resource {name} should have tags."

        try:
            check_pulumi(resource, "tags", curry)
        except AttributeError:
            return True
