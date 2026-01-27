Python 3.12.4 (tags/v3.12.4:8e8a4ba, Jun  6 2024, 19:30:16) [MSC v.1940 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> import json
... import boto3
... import uuid
... 
... # AWS Servislerini tanımla
... s3 = boto3.client('s3')
... dynamodb = boto3.resource('dynamodb')
... table = dynamodb.Table('MigrationMetadata')
... 
... def lambda_handler(event, context):
...     # S3'ten gelen tetikleyici verisini oku
...     for record in event['Records']:
...         bucket = record['s3']['bucket']['name']
...         key = record['s3']['object']['key']
...         size = record['s3']['object']['size']
...         
...         print(f"Yeni dosya tespit edildi: {key} (Bucket: {bucket})")
...         
...         # DynamoDB'ye kaydet
...         table.put_item(
...             Item={
...                 'FileID': str(uuid.uuid4()),
...                 'FileName': key,
...                 'BucketName': bucket,
...                 'FileSize': size,
...                 'Status': 'Archived-Ready'
...             }
...         )
...         
...     return {
...         'statusCode': 200,
...         'body': json.dumps('Metadata başarıyla kaydedildi!')
