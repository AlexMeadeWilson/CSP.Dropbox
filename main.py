# ----------------------------------------------
# BSCH-CSP/Dub/PT: Cloud Services and Platforms
# Student: Alex Meade Wilson (2950871)
# Programming Assignment: Dropbox using GAE
# ----------------------------------------------
import google.oauth2.id_token
from flask import Flask, render_template, request, redirect, Response, flash
from google.auth.transport import requests
from google.cloud import datastore, storage
import local_constants
import app.login.handler as loginHandler
import app.home.handler as homeHandler
import app.directory.handler as directoryHandler
import app.file.handler as fileHandler
import app.file_shared.handler as file_sharedHandler
import app.error.handler as errorHandler

app = Flask(__name__)
app.config.update(TESTING=True, SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/')
datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()

# Set the Routes for each Handler used throughout the entire Application
loginHandler.setRoutes(app)
homeHandler.setRoutes(app)
directoryHandler.setRoutes(app)
fileHandler.setRoutes(app)
file_sharedHandler.setRoutes(app)
errorHandler.setRoutes(app)

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)