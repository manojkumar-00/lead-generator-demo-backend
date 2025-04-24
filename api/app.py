from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import traceback

from .excel_utils.excel_processor import process_excel_file
from .linkedin_utils.linkedin_mock import get_linkedin_profiles
from email_utils.email_generator import generate_personalized_email
from email_utils.email_sender import send_email, schedule_followup
from linkedin_utils.lead_manager import save_lead, get_leads

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Use /tmp for file saving (required on Vercel)
UPLOAD_FOLDER = 'tmp'
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Helper to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return jsonify({
        'status': 'ok',
        'message': 'B2B Lead Generation API is running',
        'endpoints': [
            {'path': '/upload', 'method': 'POST', 'description': 'Upload Excel file with company data'},
            {'path': '/contacts', 'method': 'POST', 'description': 'Find LinkedIn profiles based on company and designation'},
            {'path': '/generate-email', 'method': 'POST', 'description': 'Generate personalized email content'},
            {'path': '/send-email', 'method': 'POST', 'description': 'Send email to contact and save lead'},
            {'path': '/leads', 'method': 'GET', 'description': 'Get all saved leads'}
        ]
    })

@app.route('/upload', methods=['POST'])
def upload_excel():
    try:
        file = request.files.get('file')
        if not file or file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400

        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        companies = process_excel_file(upload_path)
        return jsonify({'companies': companies})

    except Exception as e:
        print(e)
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

@app.route('/contacts', methods=['POST'])
def get_contacts():
    try:
        data = request.json or {}
        companies = data.get('companies')
        designation = data.get('designation')
        if not companies or not designation:
            return jsonify({'error': 'Missing companies or designation'}), 400

        profiles = get_linkedin_profiles(companies, designation)
        return jsonify({'profiles': profiles})

    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

@app.route('/generate-email', methods=['POST'])
def generate_email():
    try:
        data = request.json or {}
        name = data.get('name')
        company = data.get('company')
        designation = data.get('designation')
        if not name or not company or not designation:
            return jsonify({'error': 'Missing name, company, or designation'}), 400

        email_content = generate_personalized_email(name, company, designation)
        return jsonify({'email_content': email_content})

    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

@app.route('/send-email', methods=['POST'])
def send_email_route():
    try:
        data = request.json or {}
        email = data.get('email')
        subject = data.get('subject')
        content = data.get('content')
        contact = data.get('contact')
        if not email or not subject or not content or not contact:
            return jsonify({'error': 'Missing required fields'}), 400

        send_email(email, subject, content)
        followup_date = schedule_followup(7)

        lead_info = {
            'contact': contact,
            'email_sent': True,
            'email_content': content,
            'followup_date': followup_date,
            'status': 'Contacted'
        }
        save_lead(lead_info)

        return jsonify({
            'success': True,
            'message': 'Email sent successfully',
            'followup_date': followup_date
        })

    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

@app.route('/leads', methods=['GET'])
def get_leads_route():
    try:
        leads = get_leads()
        return jsonify({'leads': leads})
    except Exception as e:
        return jsonify({'error': str(e), 'trace': traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)