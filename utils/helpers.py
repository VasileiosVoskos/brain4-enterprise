import json
import os
from pathlib import Path
import pandas as pd
from datetime import datetime
import pytz

def load_json(file_path):
    """Load JSON data from file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_json(file_path, data):
    """Save data to JSON file"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def get_current_time():
    """Get current time in UTC"""
    return datetime.now(pytz.UTC)

def format_datetime(dt):
    """Format datetime for display"""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def validate_file(file, allowed_types):
    """Validate uploaded file type"""
    if file is None:
        return False, "No file uploaded"
    
    file_type = file.type
    if file_type not in allowed_types:
        return False, f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
    
    return True, "File valid"

def save_uploaded_file(file, directory):
    """Save uploaded file to specified directory"""
    try:
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        return True, file_path
    except Exception as e:
        return False, str(e)

def generate_mock_data():
    """Generate mock data for testing"""
    return {
        "claims": [
            {
                "id": "CLM001",
                "date": "2024-03-15",
                "amount": 5000,
                "status": "Pending",
                "type": "Accident"
            },
            {
                "id": "CLM002",
                "date": "2024-03-14",
                "amount": 3000,
                "status": "Approved",
                "type": "Theft"
            }
        ],
        "legal_cases": [
            {
                "id": "LEG001",
                "title": "Contract Dispute",
                "status": "Active",
                "priority": "High"
            },
            {
                "id": "LEG002",
                "title": "Insurance Claim",
                "status": "Pending",
                "priority": "Medium"
            }
        ]
    }# Placeholder for helpers.py
