import os
from flask import Flask, flash,render_template, request,redirect, url_for
from werkzeug import secure_filename

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'csv'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'my unobvious secret key'


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
	if request.method == 'POST':
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
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				flash('File(s) successfully uploaded')
	return render_template("upload.html" )
   


if __name__ == "__main__":
    app.run()



