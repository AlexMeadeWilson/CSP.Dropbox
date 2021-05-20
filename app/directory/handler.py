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
	app.route('/create_root', methods=['POST'])(createRootHandler)
	app.route('/add_directory/', methods=['POST'])(addDirectoryNoPrefixHandler)
	app.route('/add_directory/<path:prefix>', methods=['POST'])(addDirectoryHandler)
	app.route('/delete_directory/<path:path>', methods=['POST'])(deleteDirectoryHandler)
	app.route('/this_directory/<path:path>', methods=['GET'])(thisDirectoryHandler)

def addDirectory(directory_name):
	storage_client = storage.Client(project=local_constants.PROJECT_NAME)
	bucket = storage_client.bucket(local_constants.PROJECT_STORAGE_BUCKET)
	blob = bucket.blob(directory_name)
	blob.upload_from_string('', content_type='application/x-www-form-urlencoded;charset=UTF-8')

def deleteDirectory(path):
	storage_client = storage.Client(project=local_constants.PROJECT_NAME)
	bucket = storage_client.bucket(local_constants.PROJECT_STORAGE_BUCKET)
	blob = bucket.blob(path)
	try:
		blob.delete()
	except ValueError as exc:
		flash('Error: ', str(exc))

def thisDirectory(path):
	storage_client = storage.Client(project=local_constants.PROJECT_NAME)
	bucket = storage_client.bucket(local_constants.PROJECT_STORAGE_BUCKET)
	blob = bucket.blob(path)
	return blob

# Handlers
def createRootHandler():
	user = validateAuth()
	if user is None:
		return redirect('/login')
	try:
		root = 'rootDir/'
		addDirectory(root)

	except ValueError as exc:
		flash('Error: ', str(exc))

	return redirect('/')

def createDirectoryModel(directory_name):
	user = validateAuth()
	if user is None:
		return redirect('/login')

	entity_key = datastore_client.key('Directory', user['email'])
	entity = datastore.Entity(key=entity_key)
	entity.update({
		'dir_id': str(uuid.uuid4()),
		'dir_name': directory_name,
		'dir_created': datetime.datetime.utcnow(),
		'dir_user_id': user['uid']
	})
	datastore_client.put(entity)

def addDirectoryNoPrefixHandler():
	user = validateAuth()
	if user is None:
		return redirect('/login')

	try:
		directory_name = request.form['dir_name']
		if directory_name == '' or directory_name[len(directory_name) - 1] != '/':
			return redirect('/')
		createDirectoryModel(directory_name)
		addDirectory(directory_name)

	except ValueError as exc:
		flash('Error: ', str(exc))

	return redirect('/home/')

def addDirectoryHandler(prefix):
	user = validateAuth()
	if user is None:
		return redirect('/login')

	try:
		directory_name = prefix + request.form['dir_name']
		if directory_name == '' or directory_name[len(directory_name) - 1] != '/':
			return redirect('/')
		createDirectoryModel(directory_name)
		addDirectory(directory_name)

	except ValueError as exc:
		flash('Error: ', str(exc))

	return redirect('/home/'+prefix)

def deleteDirectoryHandler(path):
	user = validateAuth()
	if user is None:
		return redirect('/login')

	try:
		if path == '' or path[len(path) - 1] != '/':
			return redirect('/')
		deleteDirectory(path)

	except ValueError as exc:
		flash('Error: ', str(exc))

	return redirect('/')

def thisDirectoryHandler(path):
	user = validateAuth()
	if user is None:
		return redirect('/login')

	try:
		if path == '' or path[len(path) - 1] != '/':
			return redirect('/')
		thisDirectory(path)

	except ValueError as exc:
		flash('Error: ', str(exc))

	return redirect('/')