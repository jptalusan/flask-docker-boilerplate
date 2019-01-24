import redis
from rq import Worker, Connection

import config

r = redis.StrictRedis(host=config.REDIS['host'], port=config.REDIS['port'])

if __name__ == '__main__':
  with Connection(r):
    worker = Worker(config.REDIS['queues'])
    worker.work()
