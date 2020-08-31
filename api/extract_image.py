#Importing libraries---
import pandas as pd
import numpy as np
import json
from pandas.io.json import json_normalize
from django.shortcuts import render
from rest_framework.decorators import api_view,renderer_classes
from rest_framework.response import Response
from rest_framework import status
import pickle
import sys
import os
import array
import s3fs
from requests.auth import HTTPBasicAuth
from boto.s3.connection import S3Connection, Bucket, Key
import boto3
from api.config import access_key_id
from api.config import secret_access_key
from api.config import s3_region
import requests
from PIL import Image,ImageDraw
from io import BytesIO
# import phonenumbers
# from phonenumbers import carrier
# from phonenumbers.phonenumberutil import number_type
import re
# re.compile('<title>(.*)</title>')
import nltk
# nltk.download('all')
from nltk.corpus import wordnet as wn
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

@api_view(['GET'])
def getExtractImg(request):
    def extract_image(URL):
        ACCESS_KEY_ID = access_key_id()
        SECRET_ACCESS_KEY = secret_access_key()
        region = s3_region()

        res = requests.get(URL)     #Fetching URL response...
        byteObj = res.content       #Converting URL object to Byte object
        img = Image.open(BytesIO(byteObj))
        rekognition = boto3.client('rekognition', region_name = region, aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
        response = rekognition.detect_text(Image={'Bytes': byteObj})

        resp_txt = []
        for i in response['TextDetections']:
            # if 'ParentId' in i :
            if 'Id' in i and 'ParentId' not in i :
                resp_txt.append(i['DetectedText'])
        resp_key = []
        for k in range(len(resp_txt)):
            resp_key.append(k)
        my_dict = dict(zip(resp_key,resp_txt))

        for key,val in my_dict.items():
            # if re.search(r'\w+@\w+', val):
            if re.search(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', val):
                my_dict['email'] = my_dict.pop(key)
                break

        for key,val in my_dict.items():
            # if re.search(r'^[1-9]\d{2}-\d{3}-\d{4}', val):
            if re.search(r'^\+?\d[\d -]{8,12}\d', val) or re.search(r'^(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', val) or re.search(r'^[1-9]\d{2}-\d{3}-\d{4}', val) or re.search(r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}',val) or re.search(r'^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*',val) or re.search(r'^(?:(?:\+|0{0,2})91(\s*[\-]\s*)?|[0]?)?[789]\d{9}', val):
                my_dict['phone'] = my_dict.pop(key)
                break

        # nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
        # for key,val in my_dict.items():
        #     if val in nouns:
        #         my_dict['name'] = my_dict.pop(key)
        #         break
        for key,val in my_dict.items():
            if nlp(val):
                my_dict['name'] = my_dict.pop(key)
                break

        for key,val in my_dict.items():
            if re.search(r'^(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})', val):
                my_dict['url'] = my_dict.pop(key)
                break

        lst = ['email','phone','name','url']
        dict1 = {}
        unknown = []

        for m,n in my_dict.items():
            if m not in lst:
                unknown.append(n)

        newdict = {k: my_dict[k] for k in lst if k in my_dict}
        
        dict1['results'] = unknown
        dict2 = {**newdict,**dict1}
        return dict2

    if request.method == "GET":
        try:
            respImg = extract_image(request.GET.get('url'))
            return Response(respImg)
        except Exception as e:
            print(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return Response("Error in extract_image response",status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Error in GET response",status=status.HTTP_400_BAD_REQUEST)
