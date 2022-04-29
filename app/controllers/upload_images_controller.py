from flask import Flask, request
import os
import boto3

app = Flask(__name__)

client_s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("ACCESS_SECRET")
)
    
# @app.post("/upload")
def upload_images():
    file = request.files.get('file')
    
    if file is not None:
        print(type(file.filename))        
        file_upload = os.path.join('/tmp/',file.filename)
        file.save(file_upload)
        response = client_s3.upload_file(file_upload, os.getenv("BUCKET_NAME"), file.filename)
        print(response)

    return "upload realizado com sucesso"