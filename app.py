import os
import datetime
import threading
import time
from flask import Flask, jsonify, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

# Configuration: update these values accordingly.
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')  # Set this env var in your system.
FROM_EMAIL = 'davidpountney2@gmail.com'
TO_EMAILS = ['chrisatspeakerscorner@gmail.com', 'subwayheaven@gmail.com']  # List of recipients.
TEMPLATE_ID = 'd-17dae4232dd14e3dab160592b0fdc73b'

# Global variable to store the next check time
next_check_time = datetime.datetime.now() + datetime.timedelta(days=7)

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

def check_life_signal():
    """Continuously check if the current time exceeds next_check_time."""
    global next_check_time
    while True:
        if datetime.datetime.now() > next_check_time:
            send_email()
            # After sending an email, set next_check_time far in the future to prevent spam
            next_check_time = datetime.datetime.now() + datetime.timedelta(days=7)
        time.sleep(3600)  # Check every hour

@app.route('/signal-life', methods=['POST'])
def signal_life():
    """Reset the next_check_time to 7 days from now."""
    global next_check_time
    next_check_time = datetime.datetime.now() + datetime.timedelta(days=7)
    return jsonify({"message": "Life signal received", "next_check_time": next_check_time.isoformat()}), 200

@app.route('/get-time', methods=['GET'])
def get_time():
    """Return the next_check_time in a readable format."""
    return jsonify({"next_check_time": next_check_time.strftime('%A, %B %d, %Y %I:%M %p')}), 200

# Start the background checker thread
checker_thread = threading.Thread(target=check_life_signal, daemon=True)
checker_thread.start()

if __name__ == '__main__':
    # For production, consider using a WSGI server (e.g., gunicorn)
    app.run(host='0.0.0.0', port=5000)