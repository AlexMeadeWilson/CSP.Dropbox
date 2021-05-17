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
    app.route('/login', methods=['GET'])(login)
    app.route('/logout', methods=['GET'])(logout)

def login():
    user = validateAuth()
    if user is not None:
        return redirect('/')

    return render_template('login.html')

def logout():
    user = None
    if user is not None:
        return redirect('/')

    return render_template('login.html')