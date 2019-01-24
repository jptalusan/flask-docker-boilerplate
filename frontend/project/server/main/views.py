from flask import Flask, render_template, Blueprint, current_app
from flask import url_for, redirect, send_from_directory, request
from flask import jsonify
import requests
import os
import eventlet
from .. import socketio
from ..forms.upload_form import UploadForm
from ..tools import general_tools
from werkzeug.utils import secure_filename
import redis
from rq import Queue, Connection

eventlet.monkey_patch()

main_blueprint = Blueprint('main', __name__,)

@main_blueprint.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@main_blueprint.route('/test', methods=['GET'])
def test():
  url = request.url_root + '/api/receive'
  data = {"key": "valueeee"}
  r = requests.post(url, json=data)
  dictFromServer = r.json()
  return 'received response from API: ' + dictFromServer['response']

@main_blueprint.route('/redis', methods=['GET'])
def redis_test():
  r = redis.StrictRedis(host='redis', port=6380)
  r.set('KEY', 'REDIS value')
  stored_data = r.get('KEY')
  output = 'Hello ' + stored_data.decode()
  print(output)
  return output

@main_blueprint.route('/upload', methods=['GET', 'POST'])
def upload():
  form = UploadForm()
  if form.validate_on_submit():
    file = form.file.data
    if file and general_tools.allowed_file(file.filename):
      filename = secure_filename(file.filename)
      os.makedirs(os.path.join(current_app.instance_path, 'htmlfi'), exist_ok=True)
      file.save(os.path.join(current_app.instance_path, 'htmlfi', filename))
      return redirect(url_for('main.uploaded_file', filename=filename))
  return render_template('upload.html', form=form, result=None)

@main_blueprint.route('/uploads/<filename>')
def uploaded_file(filename):
  return send_from_directory(os.path.join(current_app.instance_path, 'htmlfi'), filename)

@main_blueprint.route('/iris_classifier', methods=['GET', 'POST'])
def iris_classifier():
  form = UploadForm()
  if request.method == 'POST':
    if form.validate_on_submit():
      file = form.file.data
      if file and general_tools.allowed_file(file.filename):
        filename = secure_filename(file.filename)
        os.makedirs(os.path.join(current_app.instance_path, 'htmlfi'), exist_ok=True)
        file.save(os.path.join(current_app.instance_path, 'htmlfi', filename))
        print(filename)
        url = request.url_root + 'api/iris_dist_process'
        data = {"filename": filename,
                "nodes": 1}
        print(url, data)
        r = requests.post(url, json=data)
        dictFromServer = r.json()
        return r.text
        # return 'received response from API: ' + dictFromServer['response']
  elif request.method == 'GET':
      return render_template('upload.html', form=form, result=None)

@socketio.on('my event')
def log_message(message):
    socketio.emit('my response', {'data': 'got it!'})
    print('received: ' + str(message))
