#############
### Flask app for citation notification
#############

from __future__ import print_function, division, unicode_literals
import numpy as np

from flask import Flask, jsonify, render_template, request, send_file, make_response, json

app = Flask(__name__)

@app.route('/')
def homepage():
	return render_template('index.html')

@app.route('/showSignUp')
def showsignup():
	return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signup():
	_name = request.form['inputName']
	_email = request.form['inputEmail']
	_password = request.form['inputDOI']
	if _name and _email and _password:
	    return json.dumps({'html':'<span>All fields good !!</span>'})
	else:
	    return json.dumps({'html':'<span>Enter the required fields</span>'})
	
	
if __name__ == '__main__':
	app.debug = True
	app.run()
