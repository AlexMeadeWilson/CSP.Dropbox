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
from app.login.auth_validator import validateAuth

def setRoutes(app):
	app.route('/upload_file', methods=['POST'])(uploadFileHandler)
	app.route('/download_file/<path:path>', methods=['POST'])(downloadFileHandler)
	app.route('/share_file/<path:path>', methods=['POST'])(shareFileHandler)
	app.route('/delete_file/<path:path>', methods=['POST'])(deleteFileHandler)

def addFile(file):
	storage_client = storage.Client(project=local_constants.PROJECT_NAME)
	bucket = storage_client.bucket(local_constants.PROJECT_STORAGE_BUCKET)
	blob = bucket.blob(file.filename)
	blob.upload_from_file(file)

def downloadBlob(filename):
	storage_client = storage.Client(project=local_constants.PROJECT_NAME)
	bucket = storage_client.bucket(local_constants.PROJECT_STORAGE_BUCKET)
	blob = bucket.blob(filename)
	return blob.download_as_bytes()

def deleteFile(file):
	storage_client = storage.Client(project=local_constants.PROJECT_NAME)
	bucket = storage_client.bucket(local_constants.PROJECT_STORAGE_BUCKET)
	blob = bucket.blob(file)
	try:
		blob.delete()
	except ValueError as exc:
		flash('Error: ', str(exc))

def shareFile(file):
	print("Share File incomplete.")

# ROUTE HANDLERS
def uploadFileHandler():
	user = validateAuth()
	if user is None:
		return redirect('/login')
	try:
		file = request.files['file_name']
		if file.filename == '':
			return redirect('/')
		addFile(file)
	except ValueError as exc:
		flash('Error: ', str(exc))
	return redirect('/')

def downloadFileHandler(path):
	user = validateAuth()
	if user is None:
		return redirect('/login')

	return Response(downloadBlob(path), mimetype='application/octet-stream')

def shareFileHandler(path):
	user = validateAuth()
	if user is None:
		return redirect('/login')

	try:
		shareFile(path)
	except ValueError as exc:
		flash('Error: ', str(exc))

def deleteFileHandler(path):
	user = validateAuth()
	if user is None:
		return redirect('/login')

	try:
		deleteFile(path)
	except ValueError as exc:
		flash('Error: ', str(exc))

	return redirect('/')