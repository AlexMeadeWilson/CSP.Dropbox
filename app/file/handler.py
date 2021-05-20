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
import uuid
import datetime
from app.login.auth_validator import validateAuth

datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()

def setRoutes(app):
	app.route('/upload_file/', methods=['POST'])(uploadFileNoPrefixHandler)
	app.route('/upload_file/<path:prefix>', methods=['POST'])(uploadFileHandler)
	app.route('/download_file/<path:path>', methods=['POST'])(downloadFileHandler)
	app.route('/share_file/<path:path>', methods=['POST'])(shareFileHandler)
	app.route('/delete_file/<path:path>', methods=['POST'])(deleteFileHandler)

def addFile(prefix, file):
	storage_client = storage.Client(project=local_constants.PROJECT_NAME)
	bucket = storage_client.bucket(local_constants.PROJECT_STORAGE_BUCKET)
	blob = bucket.blob(prefix + file.filename)
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

def createFileModel(file):
	user = validateAuth()
	if user is None:
		return redirect('/login')

	entity_key = datastore_client.key('File', user['email'])
	entity = datastore.Entity(key=entity_key)
	entity.update({
		'file_id': str(uuid.uuid4()),
		'file_name': file.filename,
		'file_created': datetime.datetime.utcnow(),
		'file_uid': user['uid']
	})
	datastore_client.put(entity)

def shareFile(file):
	print("Share File incomplete.")

# ROUTE HANDLERS
def uploadFileNoPrefixHandler():
	user = validateAuth()
	if user is None:
		return redirect('/login')

	prefix = ''
	try:
		file = request.files['file_name']
		if file.filename == '':
			return redirect('/')
		createFileModel(file)
		addFile(prefix, file)

	except ValueError as exc:
		flash('Error: ', str(exc))

	return redirect('/home/'+prefix)

def uploadFileHandler(prefix):
	user = validateAuth()
	if user is None:
		return redirect('/login')
	try:
		file = request.files['file_name']
		if file.filename == '':
			return redirect('/')
		createFileModel(file)
		addFile(prefix, file)

	except ValueError as exc:
		flash('Error: ', str(exc))

	return redirect('/home/'+prefix)

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