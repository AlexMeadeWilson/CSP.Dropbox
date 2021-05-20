# ----------------------------------------------
# BSCH-CSP/Dub/PT: Cloud Services and Platforms
# Student: Alex Meade Wilson (2950871)
# Programming Assignment: Dropbox using GAE
# ----------------------------------------------
import os.path
import google.oauth2.id_token
from flask import Flask, render_template, request, redirect, Response, flash
from google.auth.transport import requests
from google.cloud import datastore, storage
import local_constants
from app.login.auth_validator import validateAuth

def setRoutes(app):
    app.route('/', methods=['GET'])(home) # Returns to Root Directory
    app.route('/home', methods=['GET'])(home) # Returns to Root Directory
    app.route('/home/', methods=['GET'])(home) # Returns to Root Directory
    app.route('/home/<path:path>', methods=['GET'])(returnDirectory) # Returns a Specific Directory
    app.route('/home/<path:path>', methods=['POST'])(previousDirectory) # Returns the previous Directory

def blobList(prefix):
    user = validateAuth()
    if user is None:
        return redirect('/login')

    storage_client = storage.Client(project=local_constants.PROJECT_NAME)
    return storage_client.list_blobs(local_constants.PROJECT_STORAGE_BUCKET, prefix=prefix, delimiter='')

def returnDirectory(path):
    user = validateAuth()
    if user is None:
        return redirect('/login')

    file_list = []
    directory_list = []
    prefix = path

    try:
        blob_list = blobList(prefix)
        for i in blob_list:
            if user['uid'] in i.name:
                if i.name[len(i.name) - 1] == '/':
                    directory_list.append(i)
                else:
                    file_list.append(i)

    except ValueError as exc:
        flash('Error: ', str(exc))

    return render_template('home.html', user=user, prefix=prefix, directory_list=directory_list, file_list=file_list)

def previousDirectory(path):
    user = validateAuth()
    if user is None:
        return redirect('/login')

    file_list = []
    directory_list = []
    path = path[:-1]
    prefix = os.path.dirname(path)

    try:
        blob_list = blobList(prefix)
        for i in blob_list:
            if user['uid'] in i.name:
                if i.name[len(i.name) - 1] == '/':
                    directory_list.append(i)
                else:
                    file_list.append(i)


    except ValueError as exc:
        flash('Error: ', str(exc))

    return render_template('home.html', user=user, prefix=prefix, directory_list=directory_list, file_list=file_list)

def home():
    user = validateAuth()
    if user is None:
        return redirect('/login')

    prefix = ''
    file_list = []
    directory_list = []

    try:
        blob_list = blobList(prefix)
        for i in blob_list:
            if user['uid'] in i.name:
                if i.name[len(i.name) - 1] == '/':
                    directory_list.append(i)
                else:
                    file_list.append(i)

    except ValueError as exc:
        flash('Error: ', str(exc))

    return render_template('home.html', user=user, prefix=prefix, directory_list=directory_list, file_list=file_list)