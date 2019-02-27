from flask import Flask, render_template, Blueprint, current_app
from flask import url_for, redirect, send_from_directory, request
from flask import jsonify
import requests
import os
import eventlet
from .. import socketio, mqtt
from .forms.upload_form import UploadForm
from ..tools import general_tools
from werkzeug.utils import secure_filename
import redis
from rq import Queue, Connection

eventlet.monkey_patch()

main_blueprint = Blueprint('main', __name__, 
                           template_folder='templates', 
                           static_folder='static',
                           static_url_path='static')

@main_blueprint.route('/', methods=['GET'])
def index():
  return render_template('main/index.html')

@main_blueprint.route('/hello')
def hello():
  print("Name:", main_blueprint.name)

  url = request.url_root + url_for('api.receive')
  print(url)
  data = {"key": "valueeee"}  
  r = requests.post(url, json=data) 
  dictFromServer = r.json() 
  print('received response from API: ' + dictFromServer['response'])
  return render_template(os.path.join(main_blueprint.name, 'hello.html'))

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
  return render_template(os.path.join(main_blueprint.name, 'upload.html'), form=form, result=None)

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

        url = request.url_root + main_blueprint.name + '/api/iris_dist_process'
        data = {"filename": filename,
                "nodes": 1}
        print(url, data)
        r = requests.post(url, json=data)
        dictFromServer = r.json()
        return redirect(url_for('main.monitor'))
        # return 'received response from API: ' + dictFromServer['response']
  elif request.method == 'GET':
      return render_template(os.path.join(main_blueprint.name, 'upload.html'), form=form, result=None)

@main_blueprint.route('/monitor', methods=['GET'])
def monitor():
  mqtt.subscribe('hello')
  return render_template(os.path.join(main_blueprint.name, 'monitor.html'))

@socketio.on('my event')
def log_message(message):
  socketio.emit('my response', {'data': 'got it!'})
  print('received: ' + str(message))

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
  data = dict(
      topic=message.topic,
      payload=message.payload.decode()
  )
  print(data)
  monitor = dict(
    user_name=data['topic'],
    message=data['payload']
  )
  socketio.emit('monitor message', data=monitor)

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)