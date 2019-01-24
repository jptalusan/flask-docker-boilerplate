from dateutil import tz
import redis

def delRedisFromAllKeys(r, K):
  try:
    for key in K:
      r.delete(K)
  except:
    return false

def setRedisKV(r, K, V):
  try:
    # r = redis.StrictRedis(host="redis", port=6379, password="", decode_responses=True)
    r.set(K, V)
    return True
  except:
    return False

def incrRedisKV(r, K):
  try:
    # r = redis.StrictRedis(host="redis", port=6379, password="", decode_responses=True)
    r.incr(K)
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

def get_redis_server_time():
  # Start a redis connection
  r = redis.StrictRedis(host="redis", port=6380, password="", decode_responses=True)
  sec, microsec = r.time()
  return ((sec * 1000000) + microsec)