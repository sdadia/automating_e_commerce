from pprint import pprint
import boto3
import time
import random
from faker import Faker
import json
from cork_data_creation import StoreGenerator as CorkStoreGenerator
import random, string
import argparse

def string2numeric_hash(text):
    import hashlib
    return int(hashlib.md5(text).hexdigest()[:8], 16)

# get stream name from the commandline
parser = argparse.ArgumentParser(description="Create an AWS stream")
parser.add_argument("-s", "--stream_name", help="Name of AWS Kinesis stream you want to create", required=True)
parser.add_argument("-t", "--time", help="realtime or past", required=False, default="realtime")
args = vars(parser.parse_args())

my_producer = CorkStoreGenerator()
kinesis_client = boto3.client('kinesis', region_name='eu-west-1')

while(1):
    # generate data
    data = my_producer.generate_data_json(time=args["time"])

    record = {
        'Data':json.dumps(data, sort_keys=True) + "\n",
        'PartitionKey': data['city']
    }
    pprint(record)

    response = kinesis_client.put_record(**record, StreamName=args['stream_name'])
    pprint(response['ResponseMetadata']['HTTPStatusCode'])

    time.sleep(0.6)