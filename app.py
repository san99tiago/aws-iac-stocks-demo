#!/usr/bin/env python3
import os
import aws_cdk as cdk
from cdk.demo_stack import DemoStack


# Intentionally get the main name for the resources from the environment variables (Cloud9 or CI/CD)
try:
    MAIN_RESOURCES_NAME = os.environ.get("C9_PROJECT") or os.environ.get(
        "MAIN_RESOURCES_NAME"
    )
    MAIN_RESOURCES_NAME = (
        MAIN_RESOURCES_NAME.replace("@", "").replace(".", "").replace("_", "")
    )
except Exception as e:
    error_message = "ERROR: you need to set the environment variable 'C9_PROJECT' or 'MAIN_RESOURCES_NAME'"
    print(error_message)
    raise Exception(error_message)


app = cdk.App()
DemoStack(
    app,
    f"stocks-demo-{MAIN_RESOURCES_NAME}",
    description=f"Stack for stocks-demo {MAIN_RESOURCES_NAME} infrastructure",
    env={
        "account": os.environ.get("CDK_DEFAULT_ACCOUNT"),
        "region": "us-east-1",  # Intentionally set to 'us-east-1' due to Lambda Layer used
    },
)

app.synth()
