import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime, timedelta
import json
import time

def send_email(recipient, subject, content):
    try:
        # Parse content if it's a JSON string
        if isinstance(content, str):
            try:
                content_json = json.loads(content)
                email_subject = content_json.get('subject', subject)
                email_body = content_json.get('body', '')
            except json.JSONDecodeError:
                # If content is not valid JSON, use it as is
                email_subject = subject
                email_body = content
        else:
            # If content is already a dict
            email_subject = content.get('subject', subject)
            email_body = content.get('body', '')

        print(f"=== MOCK EMAIL SENDING ===")
        print(f"To: {recipient}")
        print(f"Subject: {email_subject}")
        print(f"Body: {email_body}")
        print(f"=== END MOCK EMAIL ===")
        
        # Simulate network delay
        time.sleep(1)
        
        # Return success response
        return {
            'success': True,
            'message': f'Email successfully sent to {recipient}'
        }
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return {
            'success': False,
            'message': f'Failed to send email: {str(e)}'
        }

def schedule_followup(days_later=7):
    followup_date = datetime.now() + timedelta(days=days_later)
    return followup_date.isoformat()

def send_actual_email(recipient, subject, body):
    try:
        # Get email credentials from environment variables
        email_user = os.environ.get('EMAIL_USER')
        email_password = os.environ.get('EMAIL_PASSWORD')
        email_server = os.environ.get('EMAIL_SERVER', 'smtp.gmail.com')
        email_port = int(os.environ.get('EMAIL_PORT', 587))
        
        if not email_user or not email_password:
            raise ValueError("Email credentials not configured")
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = recipient
        msg['Subject'] = subject
        
        # Attach body
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to server and send
        server = smtplib.SMTP(email_server, email_port)
        server.starttls()
        server.login(email_user, email_password)
        text = msg.as_string()
        server.sendmail(email_user, recipient, text)
        server.quit()
        
        return {
            'success': True,
            'message': f'Email successfully sent to {recipient}'
        }
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return {
            'success': False,
            'message': f'Failed to send email: {str(e)}'
        }
