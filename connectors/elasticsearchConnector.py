from elasticsearch import Elasticsearch
from ssl import create_default_context
import os

def connect():
    """
    Connect to ElasticSearch with environment credentials
    """
    ### Connect to Elasticsearch ###
    context = create_default_context(cafile=None)
    try:
        esClient = Elasticsearch(hosts=os.environ["elasticsearchHosts"],
                                                  http_auth=os.environ["elasticsearchHttpAuth"],
                                                  scheme=os.environ["elasticsearchScheme"],
                                                  port=os.environ["elasticsearchPort"],
                                                  ssl_context=context)
    except Exception as e:
        print('[ERROR][elasticsearchConnector]: Environ "get" error')
        print(e)
        return False
    ### Connection Check Up ###
    if esClient.ping() != True:
        print('[ERROR][elasticsearchConnector]: ElasticSearch "connect" error')
        return False
    return esClient
