#############
### Flask app for citation notification
#############

from __future__ import print_function, division, unicode_literals
import numpy as np

from flask import Flask, jsonify, render_template, request, send_file, make_response

app = Flask(__name__)

@app.route('/')
def homepage():
	return render_template('index.html')
	
if __name__ == '__main__':
	app.debug = True
	app.run()
