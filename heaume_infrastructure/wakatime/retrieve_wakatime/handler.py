import base64
import os
from datetime import datetime, timedelta

import requests
from schema import Result

URL_WAKATIME = "https://wakatime.com"
URL_API = f"{URL_WAKATIME}/api/v1"
URL_AUTHORIZATION = f"{URL_WAKATIME}/oauth"
TOKEN = os.environ["token"]


def handler(event, context):
    """Retrieve the daily time from Waketime API and format the response
    to send the payload to "write_to_influxdb" lambda.
    """
    base64_token = base64.b64encode(TOKEN.encode("ascii")).decode("ascii")
    now = datetime.strptime(event["time"], "%Y-%m-%dT%H:%M:%SZ")
    now = now - timedelta(seconds=1)
    date = now.strftime("%Y-%m-%d")

    response = requests.get(
        f"{URL_API}/users/current/durations?date={date}",
        headers={"Authorization": f"Basic {base64_token}"},
    )

    data = response.json()
    result = Result(**data)
    shards = result.merged_shards()
    points = [shard.to_influx_point(now) for shard in shards]

    return {"organization": "Heaume", "bucket": "Activity", "points": points}
