import os
from re import sub
from subprocess import check_output

from boto3 import client

backend_prefix = os.getenv('BACKEND_PREFIX', 'terraform-backend')
state_region = os.getenv('STATE_REGION', 'us-east-2')
state_prefix = os.getenv('STATE_PREFIX', '')
branch = os.getenv('GITHUB_REF_NAME').replace('/', '-')
repo = os.getenv('GITHUB_REPOSITORY')
name = sub('.*/', '', repo)
client = client('s3')
response = client.list_buckets()
buckets = []
start_directory = os.getcwd()

if os.path.exists(branch + '.tfvars'):
    os.rename(branch + '.tfvars', branch + 'auto.tfvars')

for bucket in response['Buckets']:
    if bucket["Name"].startswith(backend_prefix):
        buckets.append(bucket["Name"])

if len(buckets) == 1:
    bucket = buckets.pop()
elif len(buckets) < 1:
    os.chdir(os.path.dirname(os.path.realpath(__file__)) + '/s3')
    os.system('terraform init')
    os.system('terraform apply -auto-approve -var="bucket_prefix=' + backend_prefix + '"')
    bucket = check_output('terraform output -raw bucket', shell=True, text=True).strip()
    os.chdir(start_directory)
elif len(buckets) > 1:
    print('Multiple backends found: ', buckets)
    exit()

if not os.path.exists('backend.tf'):
    f = open('backend.tf', 'w')
    f.write('terraform {\n')
    f.write('  backend "s3" {\n')
    f.write('    bucket = "' + bucket + '"\n')
    f.write('    key    = "' + name + '/' + state_prefix + branch + '.json"\n')
    f.write('    region = "' + state_region + '"\n')
    f.write('  }\n')
    f.write('}\n')
    f.close()
