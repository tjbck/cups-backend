import sys
import os
import redis

########################
# ENV (dev,test,prod)
########################

ENV = 'dev'

if 'ENV' in os.environ:
    ENV = os.environ['ENV']

elif "pytest" in sys.modules:
    ENV = 'test'

########################
# JWT Secret
########################

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"


########################
# REDIS Setup
########################

REDIS_HOST = 'localhost' if ENV != 'prod' else 'host.docker.internal'

REDIS_PASSWORD = 'root!'
if 'REDIS_PASSWORD' in os.environ:
    REDIS_PASSWORD = os.environ['REDIS_PASSWORD']

REDIS = redis.Redis(host=REDIS_HOST, port=6379, db=0, password=REDIS_PASSWORD)

########################
# MISC
########################

UPLOAD_FOLDER_DIR = './uploads'
