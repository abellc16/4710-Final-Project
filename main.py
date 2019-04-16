# example is based on http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import jinja2
import util

# get current app directory
dir_path = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = dir_path + '/dankmemes/'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		if 'file' not in request.files:
			log = 'no file field in request.'
			return render_template('homepage.html', log = log)
		file = request.files['file']
		if file.filename == '':
			log = 'Empty filename.'
			return render_template('homepage.html', log = log)
		if file and util.allowed_file(file.filename):
			filename = secure_filename(file.filename)
			if os.path.exists(app.config['UPLOAD_FOLDER']) == False:
				os.makedirs(app.config['UPLOAD_FOLDER'])
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return render_template('homepage.html', filename=filename, column_names=column_names, data_part=data_part)
	elif request.method == 'GET':
		return render_template('homepage.html')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def get_path(path):
        return render_template(path)

@app.route('/api/request-data', methods=['GET'])
def request_parsed_file():
    filename = request.args.get('filename')
    data = pandas.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return data.to_json()

@app.route('/api/process_csv/<lower_threshold>/<upper_threshold>')
def process_csv(lower_threshold='', upper_threshold=''):
	qualified, outlier = util.threshold_process_method(app.config['DATA_FILE'], app.config['COL_NAME'], float(lower_threshold), float(upper_threshold))
	# print(qualified)
	return qualified

if __name__ == '__main__':
	app.debug = True
	ip = '127.0.0.1'
	app.run(host=ip)

