import os
import random
import csv
import io
import codecs
from flask import Flask, flash,render_template, request,redirect, url_for, jsonify
from werkzeug import secure_filename
from flask_socketio import SocketIO, emit

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'csv', 'mp4'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'my unobvious secret key'
socketio = SocketIO(app)

fileName=""
counter=0
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/dashboard")
def dashboard():
	return render_template("dashboard.html")

@app.route("/upload", methods = ['GET', 'POST'])
def upload():
	'''if request.method == 'POST':
		#check if the post request has the file part
			if 'file' not in request.files:
				flash('no file part of request')
				return redirect(request.url)
			file = request.files['file']
			if file.filename == '':
				flash('no file selected')
				return redirect(request.url)
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				fileName = request.files['file']
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				flash('File uploaded successfully')
				return redirect(url_for('dashboard'))'''
	return render_template("upload.html")

@app.route('/verify', methods=['GET','POST'])
@socketio.on("submit")
def verify():
	flask_file = request.files['file']
	if not flask_file:
		return 'Upload a CSV file'
	fileName = flask_file
	data = []
	col1 = []
	col2 = []
	stream = codecs.iterdecode(fileName.stream, 'utf-8')
	for row in csv.reader(stream, dialect=csv.excel):
		if row:
			col1.append(row[0])
			col2.append(row[1])
			headline = random.choice(["active", "inactive"])
			data.append(headline)
			global counter
			counter = counter + 0

	return render_template("verify.html", info=zip(col1, col2,data))

@socketio.on("submit")
def vot(data):
	while True:
		emit("announce", {"selection": counter}, broadcast=False)


if __name__ == '__main__':  
	app.run(debug = True)
	app.run()

