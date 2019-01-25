import redis
from rq import Worker, Connection, get_current_job
import config

r = redis.StrictRedis(host=config.REDIS['host'],
                       port=config.REDIS['port'],
                       password="", decode_responses=False)

if __name__ == '__main__':
  with Connection(r):
    worker = Worker(config.QUEUES)
    worker.work()