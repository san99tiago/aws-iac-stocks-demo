#!/bin/bash

################################################################################
# PART 1: Configure NodeJs, Python and CDK libraries
################################################################################

# Install NodeJs and Python
# -->  https://nodejs.org/en/download/
# -->  https://www.python.org/downloads/

# Verify that NodeJs/npm is installed correctly
node --version
npm --version

# Verify that Python/pip is installed correctly
python --version || python3 --version
pip --version || pip3 --version

# Install AWS-CDK globally (via NodeJs)
sudo npm install -g aws-cdk

# Verify correct install of AWS-CDK
npm list --global | grep aws-cdk


################################################################################
# PART 2: Configure the Python Dependencies for the deployment
################################################################################

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# If you are NOT in Cloud9, please set this environment variable
export MAIN_RESOURCES_NAME=san99tiago  # Note: change this to your unique name


################################################################################
# PART 3: CDK Synth and Deploy
################################################################################

cdk synth
cdk deploy

################################################################################
# PART 4 (Optional): CDK Destroy
################################################################################

cdk destroy
