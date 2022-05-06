from flask import Flask, request
import os
import boto3

app = Flask(__name__)

client_s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("ACCESS_SECRET")
)
    
def upload_images():
    file = request.files.get('file')
    bucket = os.getenv("BUCKET_NAME")
    if file is not None:        
        file_upload = os.path.join('/tmp/',file.filename)
        file.save(file_upload)
        response = client_s3.upload_file(file_upload, bucket, file.filename)
        print(response)

    return f"https://{bucket}.s3.us-east-1.amazonaws.com/{file.filename}"
