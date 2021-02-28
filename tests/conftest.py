from pulumi.runtime import set_mocks, Mocks, set_all_config
import os
import json


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """

    class MyMocks(Mocks):
        def new_resource(self, token, name, inputs, provider, id_):
            return [name + "_id", inputs]

        def call(self, token, args, provider):
            return {}

    set_mocks(MyMocks(), project="heaume")
    secrets = {"heaume:influxdbURL": "https://influx.com", "heaume:influxdbToken": "token"}
    os.environ["PULUMI_CONFIG"] = json.dumps(secrets)
