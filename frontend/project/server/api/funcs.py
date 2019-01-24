import redis
import datetime
import pandas as pd
import numpy as np

ALLOWED_EXTENSIONS = set(['png', 'txt', 'csv', 'jpg', 'data'])

def allowed_file(filename):
  return '.' in filename and \
          filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def setRedisKV(r, K, V):
  try:
    # r = redis.StrictRedis(host="redis", port=6379, password="", decode_responses=True)
    r.set(K, V)
    return True
  except:
    return False

def getRedisV(r, K):
  # r = redis.StrictRedis(host="redis", port=6379, password="", decode_responses=True)
  output = r.get(K)
  if output is not None:
    return output
  else:
    return "Empty"

def appendToListK(r, K, V):
  try:
    # r = redis.StrictRedis(host="redis", port=6379, password="", decode_responses=True)
    r.rpush(K, V)
    return True
  except:
    return False

def generate_unique_ID():
  return datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')

def df_split(in_df, nodes):
    split = in_df.shape[0] // nodes
    df_arr = []
    for g, df in in_df.groupby(np.arange(len(in_df)) // split):
        df_arr.append(df)
    return df_arr
