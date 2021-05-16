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
    app.route('/', methods=['GET'])(home)

def home():
    user = validateAuth()
    if user is None:
        return redirect('/login')

    return render_template('home.html')