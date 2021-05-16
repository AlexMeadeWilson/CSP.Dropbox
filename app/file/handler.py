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
	app.route('/upload_file', methods=['POST'])(uploadFileHandler)
	app.route('/download_file/<path:path>', methods=['POST'])(downloadFile)
	app.route('/delete_file/<path:path>', methods=['POST'])(deleteFileHandler)

def addFile(file):
	storage_client = storage.Client(project=local_constants.PROJECT_NAME)
	bucket = storage_client.bucket(local_constants.PROJECT_STORAGE_BUCKET)
	blob = bucket.blob(file.filename)
	blob.upload_from_file(file)

def deleteFile(file):
	storage_client = storage.Client(project=local_constants.PROJECT_NAME)
	bucket = storage_client.bucket(local_constants.PROJECT_STORAGE_BUCKET)
	blob = bucket.blob(file)
	try:
		blob.delete()
	except ValueError as exc:
		error_message = str(exc)

def downloadBlob(filename):
	storage_client = storage.Client(project=local_constants.PROJECT_NAME)
	bucket = storage_client.bucket(local_constants.PROJECT_STORAGE_BUCKET)
	blob = bucket.blob(filename)
	return blob.download_as_bytes()

# ROUTE HANDLERS
def uploadFileHandler():
	user = validateAuth()
	if user is None:
		return redirect('/login')
	else:
		try:
			file = request.files['file_name']
			if file.filename == '':
				return redirect('/')
			addFile(file)
		except ValueError as exc:
			error_message = str(exc)
	return redirect('/')

def downloadFile(path):
	user = validateAuth()
	if user is None:
		return redirect('/login')

	return Response(downloadBlob(path), mimetype='application/octet-stream')

def deleteFileHandler(path):
	user = validateAuth()
	if user is None:
		return redirect('/login')
	else:
		try:
			deleteFile(path)
		except ValueError as exc:
			error_message = str(exc)

	return redirect('/')