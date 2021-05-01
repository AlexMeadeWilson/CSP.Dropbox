import datetime
import google.oauth2.id_token
from flask import Flask, render_template, request, redirect
from google.cloud import datastore
from google.auth.transport import requests

app = Flask(__name__)
datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()

def retrieveUserInfo(claims):
	entity_key = datastore_client.key('UserInfo', claims['email'])
	entity = datastore_client.get(entity_key)
	return entity

def createUserInfo(claims):
	entity_key = datastore_client.key('UserInfo', claims['email'])
	entity = datastore.Entity(key = entity_key)
	entity.update({
		'email': claims['email'],
		'name': claims['name'],
		'creation_date': datetime.datetime.now(),
		'bool_value': True,
		'float_value': 3.14,
		'int_value': 10,
		'string_value': 'this is a sample string',
		'list_value': [1, 2, 3, 4],
		'dictionary_value': {'A': 1, 'B': 2, 'C': 3}
	})
	datastore_client.put(entity)

def updateUserInfo(claims, new_string, new_int, new_float):
	entity_key = datastore_client.key('UserInfo', claims['email'])
	entity = datastore_client.get(entity_key)
	entity.update({
		'string_value': new_string,
		'int_value': new_int,
		'float_value': new_float
	})
	datastore_client.put(entity)

def fetch_times(email, limit):
	ancestor_key = datastore_client.key('User', email)
	query = datastore_client.query(kind='visit', ancestor=ancestor_key)
	query.order = ['-timestamp']
	times = query.fetch(limit=limit)
	return times

@app.route('/')
def root():
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
		except ValueError as exc:
			error_message = str(exc)

	return render_template('index.html', user_data=claims, error_message=error_message, user_info=user_info)

@app.route('/edit_user_info', methods=['POST'])
def editUserInfo():
	id_token = request.cookies.get("token")
	error_message = None
	claims = None
	user_info = None
	if id_token:
		try:
			claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
			new_string = request.form['string_update']
			new_int = request.form['int_update']
			new_float = request.form['float_update']
			updateUserInfo(claims, new_string, new_int, new_float)

		except ValueError as exc:
			error_message = str(exc)

	return redirect("/")

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8080, debug=True)