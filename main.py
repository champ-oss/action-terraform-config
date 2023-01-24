import os
import re

# noinspection PyPackageRequirements
from decouple import config

backend_prefix = config('BACKEND_PREFIX', default='terraform-backend')
state_prefix = config('STATE_PREFIX', default='')
branch = config('GITHUB_REF_NAME').replace('/', '-')
repo = config('GITHUB_REPOSITORY')
name = re.sub('.*/', '', repo)

if os.path.exists(branch + '.tfvars'):
    os.rename(branch + '.tfvars', branch + 'auto.tfvars')
