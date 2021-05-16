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

datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()

def retrieveUserInfo(claims):
	entity_key = datastore_client.key('UserInfo', claims['email'])
	entity = datastore_client.get(entity_key)
	return entity

def createUserInfo(claims):
	entity_key = datastore_client.key('UserInfo', claims['email'])
	entity = datastore.Entity(key=entity_key)
	entity.update({
		'email': claims['email'],
		'name': claims['name']
	})
	datastore_client.put(entity)

def validateAuth():
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    user_info = None

    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)

            user_info = retrieveUserInfo(claims)
            if user_info == None:
                createUserInfo(claims)
                user_info = retrieveUserInfo(claims)
            print(user_info)
            return user_info

        except ValueError as exc:
            flash('Error: ', str(exc))
            return None