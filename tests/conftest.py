import json
import os

from pulumi.runtime import Mocks, set_mocks


def pytest_sessionstart():
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """

    class MyMocks(Mocks):
        """The mock object for pulumi.

        .. info:: For more information: https://www.pulumi.com/docs/guides/testing/unit/
        """

        def new_resource(self, type_, name, inputs, provider, id_):
            """See Mocks.new_resource"""
            return [name + "_id", inputs]

        def call(self, token, args, provider):
            """See Mocks.call"""
            return {}

    set_mocks(MyMocks(), project="heaume")
    secrets = {
        "heaume:influxdbURL": "https://influx.com",
        "heaume:influxdbToken": "token",
        "heaume:wakatimeToken": "token",
    }
    os.environ["PULUMI_CONFIG"] = json.dumps(secrets)
