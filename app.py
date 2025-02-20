import os
from flask import Flask, jsonify, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

# Configuration: update these values accordingly.
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')  # Set this env var in your system.
FROM_EMAIL = 'davidpountney2@gmail.com'
TO_EMAILS = ['chrisatspeakerscorner@gmail.com', 'subwayheaven@gmail.com']  # List of recipients.
TEMPLATE_ID = 'd-17dae4232dd14e3dab160592b0fdc73b'

def send_email():
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        
        # Create email object with dynamic template
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=TO_EMAILS
        )
        
        # Attach template ID
        message.template_id = TEMPLATE_ID

        # Send the email
        response = sg.send(message)
        
        return f"Email sent! Status Code: {response.status_code}"
    
    except Exception as e:
        return f"Failed to send email: {e}"

@app.route('/send-email', methods=['POST'])
def trigger_email():
    # Optionally, add authentication or validation here.
    send_email()
    return jsonify({'status': 'Email triggered'}), 200

if __name__ == '__main__':
    # For production, consider using a WSGI server (e.g., gunicorn)
    app.run(host='0.0.0.0', port=5000)