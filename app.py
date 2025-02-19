import os
from flask import Flask, jsonify, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

# Configuration: update these values accordingly.
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')  # Set this env var in your system.
FROM_EMAIL = 'davidpountney2@gmail.com'
TO_EMAILS = ['chrisatspeakerscorner@gmail.com', 'subwayheaven@gmail.com']  # List of recipients.

def send_email():
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=TO_EMAILS,
        subject='Automated Email Trigger',
        html_content='<strong>This is a preconfigured email sent via SendGrid.</strong>'
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print('Email sent:', response.status_code)
    except Exception as e:
        print('Error sending email:', e)

@app.route('/send-email', methods=['POST'])
def trigger_email():
    # Optionally, add authentication or validation here.
    send_email()
    return jsonify({'status': 'Email triggered'}), 200

if __name__ == '__main__':
    # For production, consider using a WSGI server (e.g., gunicorn)
    app.run(host='0.0.0.0', port=5000)