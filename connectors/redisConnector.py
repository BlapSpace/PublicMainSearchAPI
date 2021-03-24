import redis
import os

def connect(db):
    """
    Connect to Redis with environment credentials and use the db
    """
    ### Connect to Redis ###
    try:
        redisClient = redis.Redis(host=os.environ["redisIP"],
                                                  port=os.environ["redisPort"],
                                                  password=os.environ["redisPass"],
                                                  db=db,
                                                  decode_responses=True)
    except Exception as e:
        print('[ERROR][redisConnector]: Environ "get" error')
        print(e)
        return False
    ### Connection Check Up ###
    try:
        redisClient.ping()
    except Exception as e:
        print('[ERROR][redisConnector]: Redis "connect" error')
        print(e)
        return False
    return redisClient