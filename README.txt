
STEP 1: Install Python (Download from python.org)

STEP 2: Extract this ZIP file

STEP 3: Open Command Prompt inside project folder

STEP 4: Install Django
pip install -r requirements.txt

STEP 5: Run server
python manage.py runserver

STEP 6: Open Postman

POST URL:
http://127.0.0.1:8000/assign-order/

Body (raw JSON):
{
    "restaurant_lat": 17.3850,
    "restaurant_lng": 78.4867
}

You will receive assigned partner JSON response.
