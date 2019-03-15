# Upgrading AWS CLI in Amazon Linux to the latest version.

import os
print('Current AWS CLI version:')
os.system('aws --version')

os.system('sudo yum -y install python-pip')
os.system('sudo pip uninstall awscli -y')
os.system('curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"')
os.system('unzip awscli-bundle.zip')
os.system('sudo ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws')

print("AWS CLI successfully updated, CLI version:")
os.system('aws --version')
