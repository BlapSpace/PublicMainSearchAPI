import json
import os
from bson import json_util


def send(serviceName, databases, internalErrorCode, feedback, process, timeAndDate, timeCount, statusLevel):
    ### ElasticSearch ###
    if databases[0] != False:
        for tryNum in range(1, 4):
            statusResponse = databases["elasticsearch"].index(index="servicesStatusReport", body={"tryNum": tryNum, "tryType": "ElasticSearch", "service": serviceName,
                                                                                                  "timeAndDate": timeAndDate, "timeCount": timeCount, "statusLevel": statusLevel, "internalErrorCode": internalErrorCode, "process": process, "feedback": feedback})["result"]
            if statusResponse == "created":
                return None
        print('[ERROR][servicesStatusReport]: ElasticSearch "index" error')
    ### MongoDB ###
    if databases[1] != False:
        for tryNum in range(1, 4):
            try:
                databases["mongoDB"]["servicesStatusReportFallback"].insert_one(
                    {"tryNum": tryNum, "tryType": "MongoDB", "service": serviceName, "timeAndDate": timeAndDate, "timeCount": timeCount, "statusLevel": statusLevel, "internalErrorCode": internalErrorCode, "process": process, "feedback": feedback})
                return None
            except Exception as e:
                pass
        print('[ERROR][servicesStatusReport]: MongoDB "insert_one" error')
        print(e)
    ### Redis ###
    if databases[2] != False:
        for tryNum in range(1, 4):
            try:
                databases["redisServiceStatusReport"].lpush("servicesStatusReportFallback", json.dumps(
                    {"tryNum": tryNum, "tryType": "Redis", "service": serviceName, "timeAndDate": timeAndDate, "timeCount": timeCount, "statusLevel": statusLevel, "internalErrorCode": internalErrorCode, "process": process, "feedback": feedback}, default=json_util.default))
                return None
            except Exception as e:
                print(e)
        print('[ERROR][servicesStatusReport]: Redis "lpush" error')
        print(e)
    print("[ERROR][servicesStatusReport]: All databases for servicesStatusReport(Fallback) are broken")
    # exit()

# Retryss?
