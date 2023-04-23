from flask import Flask
import boto3

from botocore.exceptions import ClientError
import logging

# create S3 bucket instance
s3 = boto3.client('s3')


def create_bucket(bucket_name):
   try:

            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
            # define the policy
            bucket_policy = {
             'Version': '2012-10-17',
             'Statement': [{
             'Sid': 'permission_statement',
             'Effect': 'Allow',
             'Principal': '*',
             'Action': ['s3:GetObject'],
             'Resource': "arn:aws:s3:::%s/*" % bucket_name
      }]
  }
      
   except ClientError as e:
        logging.error(e)
        return False
        return True
  
def uploadToS3(filename, bucketname):
             s3.upload_file(
                    Bucket = bucketname,
                    Filename=filename,
                    Key = filename
                )
             
    