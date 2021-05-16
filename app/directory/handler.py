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
from app.login.auth_validator import validateAuth

def setRoutes(app):
	app.route('/add_directory', methods=['POST'])(addDirectoryHandler)

def addDirectory(directory_name):
	storage_client = storage.Client(project=local_constants.PROJECT_NAME)
	bucket = storage_client.bucket(local_constants.PROJECT_STORAGE_BUCKET)
	blob = bucket.blob(directory_name)
	blob.upload_from_string('', content_type='application/x-www-form-urlencoded;charset=UTF-8')

def addDirectoryHandler():
	user = validateAuth()
	if user is None:
		return redirect('/login')
	else:
		try:
			directory_name = request.form['dir_name']
			if directory_name == '' or directory_name[len(directory_name) - 1] != '/':
				return redirect('/')
			addDirectory(directory_name)

		except ValueError as exc:
			error_message = str(exc)

	return redirect('/')