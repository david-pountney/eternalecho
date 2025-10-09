# eternalecho
A program to detect when I'm dead and automate sending out useful emails to inform my family etc.

ssh command is; ssh david@raspberrypi

Public API's are;

get-time (returns the date/time that the main event is triggered)
signal-life (extends the date/time when the main event is triggered)

curl -X GET http://eternalecho.ddns.me:5000/get-time
curl -X POST http://eternalecho.ddns.me:5000/signal-life

Service to send out predefined template emails;
https://login.sendgrid.com/

To check the web server is running correctly run this command through SSH;

sudo systemctl status flask_app.service

To check the dynamic IP redirector run the command through SSH;

sudo systemctl status noip-duc.service
