import pymongo
import os

def connect():
    """
    Connect to MongoDB with environment credentials
    """
    ### Connect to MongoDB ###
    
    try:
        mongoDBClient = pymongo.MongoClient(host=os.environ["mongoDBIP"],
                                                                               username=os.environ["mongoDBUsername"],
                                                                               password=os.environ["mongoDBPassword"],
                                                                               authSource=os.environ["mongoDBAuthSource"],
                                                                               authMechanism=os.environ["mongoDBAuthMechanism"])
    except Exception as e:
        print('[ERROR][mongoDBConnector]: Environ "get" error')
        print(e)
        return False
    ### Connection Check Up ###
    try:
        mongoDBClient.server_info()
    except Exception as e:
        print('[ERROR][mongoDBConnector]: MongoDB "connect" error')
        print(e)
        return False
    return mongoDBClient