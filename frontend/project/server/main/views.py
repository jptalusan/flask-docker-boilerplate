from flask import Flask, render_template, Blueprint, current_app
from flask import url_for, redirect, send_from_directory
import requests
import os
import eventlet
from .. import socketio
from ..forms.upload_form import UploadForm
from . import functions
from werkzeug.utils import secure_filename

eventlet.monkey_patch()

main_blueprint = Blueprint('main', __name__,)

@main_blueprint.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@main_blueprint.route('/upload', methods=['GET', 'POST'])
def upload():
  form = UploadForm()
  if form.validate_on_submit():
    file = form.file.data
    if file and functions.allowed_file(file.filename):
      filename = secure_filename(file.filename)
      os.makedirs(os.path.join(current_app.instance_path, 'htmlfi'), exist_ok=True)
      file.save(os.path.join(current_app.instance_path, 'htmlfi', filename))
      return redirect(url_for('main.uploaded_file', filename=filename))
  return render_template('upload.html', form=form, result=None)

@main_blueprint.route('/uploads/<filename>')
def uploaded_file(filename):
  return send_from_directory(os.path.join(current_app.instance_path, 'htmlfi'), filename)

@socketio.on('my event')
def log_message(message):
    print('received: ' + str(message))
    socketio.emit('my response', {'data': 'got it!'})
