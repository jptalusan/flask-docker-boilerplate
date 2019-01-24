import redis
import datetime
import requests
from dateutil import tz

from ..api import funcs
from ..defs import *

def initialize_query(total, count_suffix=NODE_COUNT, done_count_suffix=DONE_NODE_COUNT):
  r = redis.StrictRedis(host="redis", port=6380, password="", decode_responses=True)

  unique_id = funcs.generate_unique_ID()
  funcs.setRedisKV(r, unique_id, 'ongoing')
  funcs.setRedisKV(r, unique_id + count_suffix, total)
  funcs.setRedisKV(r, unique_id + done_count_suffix, 0)

  return unique_id

def get_current_time():
  HERE = tz.gettz('Asia/Tokyo')
  UTC = tz.gettz('UTC')

  ts = datetime.datetime.utcnow().replace(tzinfo=UTC).astimezone(HERE)
  # local_time = ts.strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')
  local_time = ts.strftime('%Y-%m-%d %H:%M:%S.%f %Z')[:-3]
  return local_time

def get_redis_server_time():
  # Start a redis connection
  r = redis.StrictRedis(host="redis", port=6379, password="", decode_responses=True)
  sec, microsec = r.time()
  return ((sec * 1000000) + microsec)
