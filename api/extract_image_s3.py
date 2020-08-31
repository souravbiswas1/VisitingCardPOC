#Importing libraries---
import pandas as pd
import numpy as np
import json
# from bson import json_util
from django.shortcuts import render
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.response import Response
from rest_framework import status
import pickle
import requests
import sys
import os
import array
import s3fs
from requests.auth import HTTPBasicAuth
from boto.s3.connection import S3Connection, Bucket, Key
import boto3
from api.config import access_key_id
from api.config import secret_access_key
from api.config import s3_bucket_name
from api.config import s3_region

@api_view(['GET'])
def getExtractImgS3(request):
    def extract_image(x):
        ACCESS_KEY_ID = access_key_id()
        SECRET_ACCESS_KEY = secret_access_key()
        bucket = s3_bucket_name()
        region = s3_region()
        # connect to s3 client and list objects in bucket:
        # s3 = boto3.client('s3', region_name = region, aws_access_key_id = ACCESS_KEY_ID, aws_secret_access_key = SECRET_ACCESS_KEY)
        # bucket_response = s3.list_objects_v2(Bucket=bucket)
        # for i in bucket_response['Contents']:
        #     y = i['Key']
        # print(y)
        rekognition = boto3.client('rekognition', region_name = region, aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
        response = rekognition.detect_text(Image={'S3Object': {'Bucket': bucket,'Name':x}})
        resp_str = ""
        for resp in response['TextDetections']:
            if 'ParentId' in resp:
                resp_str += resp['DetectedText']+' '
        key = ['Text']
        val = [resp_str]
        keyval = dict(zip(key,val))
        return keyval

    if request.method == "GET":
        try:
            respImg = extract_image(request.GET.get('image_name'))
            return Response(respImg)
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return Response("Error in extract_image response",status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Error in GET response",status=status.HTTP_400_BAD_REQUEST)
