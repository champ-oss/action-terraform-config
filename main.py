from os import rename
from os.path import exists
from re import sub

from boto3 import client
# noinspection PyPackageRequirements
from decouple import config

backend_prefix = config('BACKEND_PREFIX', default='terraform-backend')
state_prefix = config('STATE_PREFIX', default='')
branch = config('GITHUB_REF_NAME').replace('/', '-')
repo = config('GITHUB_REPOSITORY')
name = sub('.*/', '', repo)
client = client('s3')
response = client.list_buckets()
buckets = []

if exists(branch + '.tfvars'):
    rename(branch + '.tfvars', branch + 'auto.tfvars')

for bucket in response['Buckets']:
    if bucket["Name"].startswith(backend_prefix):
        buckets.append(bucket["Name"])

if len(buckets) == 1:
    bucket = buckets.pop()
elif len(buckets) < 1:
    print('find bucket')
elif len(buckets) > 1:
    print('Multiple backends found: ', buckets)
    exit()
