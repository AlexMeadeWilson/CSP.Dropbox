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
import app.file.handler as fileHandler
import app.directory.handler as directoryHandler

def setRoutes(app):
    app.route('/', methods=['GET'])(home)
    app.route('/home', methods=['GET'])(home)

def blobList(prefix):
	storage_client = storage.Client(project=local_constants.PROJECT_NAME)
	return storage_client.list_blobs(local_constants.PROJECT_STORAGE_BUCKET, prefix=prefix)

def home():
    user = validateAuth()
    if user is None:
        return redirect('/login')
    else:
        file_list = []
        directory_list = []
        blob_list = blobList(None)
        for i in blob_list:
            if i.name[len(i.name) - 1] == '/':
                directory_list.append(i)
            else:
                file_list.append(i)

    return render_template('home.html', user=user, file_list=file_list, directory_list=directory_list)