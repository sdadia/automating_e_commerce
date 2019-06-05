import pandas as pd
import boto3
from sqlalchemy import create_engine
import pytz
my_timezone = pytz.timezone('Europe/Dublin')


# creeate s3 connection
client = boto3.client('s3', 'eu-west-1')

# create database connetion
POSTGRES_USERNAME = 'sahil'
POSTGRES_PASSWORD = 'zxcvbnm1234'
POSTGRES_DBNAME = 'data'
POSTGRES_HOST = 'superset.cznthudneeub.eu-west-1.rds.amazonaws.com'
url = 'postgresql://{}:{}@{}:{}/{}'.format(POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_HOST, 5432, POSTGRES_DBNAME)
engine = create_engine(url)
print(url)


def lambda_handler(event, context):
	for record in event['Records']:
		bucket_name = record['s3']['bucket']['name']
		print('Bucket name is : {}'.format(bucket_name))
		key = record['s3']['object']['key']
		print('File name is : {}'.format(key))
		print(key)

		# load json file
		file_name = 's3://' + bucket_name + '/' + key
		print('File name to load is : {}'.format(file_name))
		df = pd.read_json(file_name, lines=True)
		print(df.head())
		print(df.shape)
		print(df.info())
		

		# set the type of each column
		df['timestamp'] = pd.to_datetime(df['timestamp'])
		df['timestamp'] = df['timestamp'].dt.tz_localize(my_timezone)

		# send send this data to postgres
		print('sending data to postgres')
		df.to_sql('overall_data', if_exists='append', con=engine, index=False)
		print('Done sending data')

		print('\n\n\n\nxxxxxxxxxxxxx\n\n\n')


