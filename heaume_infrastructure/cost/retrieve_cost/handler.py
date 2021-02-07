from datetime import datetime, timedelta

import boto3


def handler(event, context):
    """Retrieve the daily cost from Cost Explorer API and format the response
    to send the payload to "write_to_influxdb" lambda.
    """
    client = boto3.client("ce")
    now = datetime.today()
    response = client.get_cost_and_usage(
        TimePeriod={
            "Start": (now - timedelta(days=1)).strftime("%Y-%m-%d"),
            "End": now.strftime("%Y-%m-%d"),
        },
        Granularity="DAILY",
        Metrics=["NET_AMORTIZED_COST"],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}],
    )

    result = {"organization": "Heaume", "bucket": "Cost", "points": []}

    for groups in response["ResultsByTime"][0]["Groups"]:
        result["points"].append(
            {
                "measurement": groups["Keys"][0],
                "timestamp": int(now.timestamp()),
                "fields": {
                    "amount": float(groups["Metrics"]["NetAmortizedCost"]["Amount"])
                },
                "tags": {
                    "provider": "AWS",
                    "unit": groups["Metrics"]["NetAmortizedCost"]["Unit"],
                },
            }
        )

    return result
