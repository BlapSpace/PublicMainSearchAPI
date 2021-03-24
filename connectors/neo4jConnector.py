from neo4j import GraphDatabase
import os

def connect():
    """
    Connect to Neo4j with environment credentials
    """
    ### Connect to Redis ###
    try:
        neo4jClient = GraphDatabase.driver(os.environ["neo4jURI"],
                                                                        auth=(os.environ["neo4jUsername"],
                                                                                   os.environ["neo4jPassword"]),
                                                                        encrypted=os.environ["neo4jEncrypted"],
                                                                        trust=os.environ["neo4jTrust"])
    except Exception as e:
        print('[ERROR][neo4jConnector]: Environ "get" error')
        print(e)
        return False
    ### Connection Check Up ###
    #ToDo: Self Check
    #ToDo: If error => Print it
    return neo4jClient