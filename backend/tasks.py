import time
from rq import get_current_job, Queue, Connection
import socket
import pandas as pd
from sklearn import svm
from sklearn.externals import joblib
from io import StringIO
import redis

import config
import funcs

def classify_iris_dist(input_data, nodes, unique_ID, sequence_ID):
  job = get_current_job()
  redis_connection = redis.StrictRedis(host=config.REDIS['host'],
                                       port=config.REDIS['port'],
                                       password="", decode_responses=True)

  tic = time.clock()

  funcs.appendToListK(redis_connection, unique_ID + NODES, job.id)

  input_dataIO = StringIO(input_data.decode("utf-8"))
  job.meta['handled_by'] = socket.gethostname()
  job.meta['handled_time'] = get_current_time()
  job.meta['progress'] = 0.0
  job.meta['unique_ID'] = unique_ID
  job.save_meta()

  df = pd.read_csv(input_dataIO, header=None)
  print(df.shape)

  clf = joblib.load('models/SVM_iris.pkl')
  prob = clf.predict_proba(df)

  df_prob = pd.DataFrame(prob)
  prob_idx = df_prob.idxmax(axis=1)

  toc = time.clock()
  job.meta['progress'] = toc - tic
  job.save_meta()
  iris_classes = ['setosa', 'versicolor', 'virginica']

  output = [iris_classes[x] for x in prob_idx]
  print(output)

  funcs.incrRedisKV(redis_connection, unique_ID + DONE_NODE_COUNT)
  node_count = funcs.getRedisV(redis_connection, unique_ID + NODE_COUNT)
  done_node_count = funcs.getRedisV(redis_connection, unique_ID + DONE_NODE_COUNT)

  if node_count == done_node_count:
    funcs.setRedisKV(redis_connection, unique_ID, "finished")
    with Connection(redis_connection):
      q = Queue('aggregator')
      t = q.enqueue('tasks.aggregate_data', unique_ID)
  else:
    print('still not done processing')

  return { 'sequence_ID': sequence_ID, 'output': output }
