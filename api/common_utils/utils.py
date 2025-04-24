import os
import json
import base64
import re
from datetime import datetime, timedelta

def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def format_date(date_string):
    try:
        date_obj = datetime.fromisoformat(date_string)
        return date_obj.strftime("%b %d, %Y")
    except (ValueError, TypeError):
        return date_string

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def get_days_until_followup(followup_date):
    try:
        followup = datetime.fromisoformat(followup_date)
        now = datetime.now()
        delta = followup - now
        return max(0, delta.days)
    except (ValueError, TypeError):
        return 0

def encode_file_to_base64(file_path):
    try:
        with open(file_path, "rb") as file:
            encoded = base64.b64encode(file.read())
            return encoded.decode('utf-8')
    except Exception as e:
        print(f"Error encoding file: {str(e)}")
        return None

def decode_base64_to_file(base64_string, output_path):
    try:
        with open(output_path, "wb") as file:
            file.write(base64.b64decode(base64_string))
        return True
    except Exception as e:
        print(f"Error decoding base64: {str(e)}")
        return False
