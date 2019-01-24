import redis
from rq import Queue, Connection
from . import funcs
import multiprocessing
from flask import Flask, Blueprint, request, jsonify, current_app
import pandas as pd
import os
from . import utils

api_blueprint = Blueprint('api', __name__,)

def enqueue_task(queue, unique_id, seq_id, model, sensor_list, param_list, columns, values):
  r = redis.StrictRedis(host='redis', port=6380)
  with Connection(r):
    q = Queue('default')
    task = q.enqueue('tasks.iris_classify', unique_id, seq_id,
                      model, sensor_list, param_list,
                      columns, values)
  queue.put(task.get_id())
  return

@api_blueprint.route('/receive', methods=['POST'])
def receive():
  data = request.get_json(force=True)
  print(data['key'])
  response = {'response': 'hello from the api side'}
  return jsonify(response)

#Should work as long as you have access to this url, no flask needed
@api_blueprint.route('/iris_dist_process', methods=['POST'])
def iris_dist_process():
  data = request.get_json(force=True)
  filename = data['filename']
  nodes = data["nodes"]
  r = redis.StrictRedis(host='redis', port=6380)
  print(filename)
  try:
    if filename and funcs.allowed_file(filename):
      unique_id = utils.initialize_query(nodes)
      with open(os.path.join(current_app.instance_path, 'htmlfi', filename)) as f:
        df = pd.read_csv(f, header=None)
        print(df.shape)
        df_arr = funcs.df_split(df, nodes)
        print(len(df_arr))
        processes = []
        mpq = multiprocessing.Queue()
        for df in df_arr:
          #p = multiprocessing.Process(target=enqueue_task,
          #                            args=(mpq, unique
          print(unique_id)
#        q = Queue(r)
#        #Split file into 3
#        files = funcs.split(filename, 3)
#
#        funcs.setRedisKV(redis_conn, u_ID, 'ongoing')
#        funcs.setRedisKV(redis_conn, u_ID + NODE_COUNT, nodes)
#        funcs.setRedisKV(redis_conn, u_ID + DONE_NODE_COUNT, 0)
#
#        #assuming the files are in sequential order, we can send some sequence id to the queue
#        for sequence_ID, file in enumerate(files):
#          data = file.read()
#          #Need to decode?
#          #Race condition i think.
#          task = q.enqueue('tasks.classify_iris_dist', data, nodes, u_ID, sequence_ID)
      response = {'response': 'classification'}
      return jsonify(response)
  except IOError:
    pass
  return "Unable to read file"
