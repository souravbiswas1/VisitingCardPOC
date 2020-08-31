
##Setup
pip install -r requirements.txt

##Generate static assets
python manage.py collectstatic

##Sample API Call
localhost:8000/aiml/poc/getExtractImg?url=https://5.imimg.com/data5/QS/VL/MY-3646410/visiting-card-500x500.png
