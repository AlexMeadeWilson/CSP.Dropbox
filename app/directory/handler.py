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
	app.route('/create_root', methods=['POST'])(createRootHandler)
	app.route('/add_directory', methods=['POST'])(addDirectoryHandler)
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

def addDirectoryHandler():
	user = validateAuth()
	if user is None:
		return redirect('/login')
	try:
		directory_name = user['uid'] + request.form['dir_name']
		if directory_name == '' or directory_name[len(directory_name) - 1] != '/':
			return redirect('/')
		addDirectory(directory_name)

	except ValueError as exc:
		flash('Error: ', str(exc))

	return redirect('/')

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