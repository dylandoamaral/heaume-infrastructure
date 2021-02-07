import pulumi_aws as aws

availability_zones = [az for az in aws.get_availability_zones(state="available").names]
