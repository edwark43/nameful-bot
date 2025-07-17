import os, json
from datetime import datetime

def calculate_countdown(date):
    d1 = datetime.today()
    d2 = datetime.strptime(date, "%m/%d/%Y")
    return (d2 - d1).days

def get_json():
    with open(os.getenv('JSON')) as json_data:
        d = json.load(json_data)
        return d
