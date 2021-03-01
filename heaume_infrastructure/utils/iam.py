from typing import List

from pulumi import Output

from heaume_infrastructure.utils.service import Service


def policy_invoke_lambdas(arns: Output) -> str:
    def curry(arns):
        assert len(arns) > 0, "The policy should invoke at least one lambda."
        policy_arns = ",\n".join([f'"{arn}"' for arn in arns])

        return """{
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "lambda:InvokeFunction"
                    ],
                    "Resource": [%s]
                }
            ]
        }""" % (
            policy_arns
        )

    return arns.apply(curry)
