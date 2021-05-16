# ----------------------------------------------
# BSCH-CSP/Dub/PT: Cloud Services and Platforms
# Student: Alex Meade Wilson (2950871)
# Programming Assignment: Dropbox using GAE
# ----------------------------------------------
import google.oauth2.id_token
from flask import Flask, render_template, request, redirect, Response
from google.auth.transport import requests
from google.cloud import datastore, storage
import local_constants
import app.login.handler as login
import app.home.handler as home

app = Flask(__name__)
datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()

login.setRoutes(app)
home.setRoutes(app)

@app.route('/404', methods=['GET'])
def not_found():
	return render_template('404.html')

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)