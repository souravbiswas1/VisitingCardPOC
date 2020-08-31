
import requests
from requests.auth import HTTPBasicAuth

def access_key_id():
	ACCESS_KEY_ID = ''
	return ACCESS_KEY_ID

def secret_access_key():
	SECRET_ACCESS_KEY = ''
	return SECRET_ACCESS_KEY

def s3_bucket_name():
	bucket = ''
	return bucket

def s3_region():
	s3Region = ''
	return s3Region

def tesseract_path():
	pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
	return pytesseract.pytesseract.tesseract_cmd
