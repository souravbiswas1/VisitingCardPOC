from django.contrib import admin
from django.urls import path,include
from . import extract_image,upload_image,extract_image_s3,transcribe,extract_ocr
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('getExtractImg', extract_image.getExtractImg),
    path('getUploadImg', upload_image.getUploadImg),
    path('getExtractImgS3', extract_image_s3.getExtractImgS3),
    path('getTranscribe', transcribe.getTranscribe),
    path('getExtractOcr', extract_ocr.getExtractOcr),
]
