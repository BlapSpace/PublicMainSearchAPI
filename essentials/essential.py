from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json, os, sys, inspect, time, datetime
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from essentials import servicesStatusReport
from connectors import elasticsearchConnector, mongoDBConnector, redisConnector

### Exception Handling Class ###

class UnicornException(Exception):
    def __init__(self, internalErrorCode: str, errorContext: str, statusCode: str):
        self.internalErrorCode = internalErrorCode
        self.errorContext = errorContext
        self.statusCode = statusCode

### Init essentials ###

def init(serviceName):
    ### Connect to Databases and return the clients at the end ###
    esClient = elasticsearchConnector.connect()
    mongoDBClient = mongoDBConnector.connect()
    redisClient = redisConnector.connect(15)
    databases = {"elasticsearch": esClient, "mongoDB": mongoDBClient, "redisServiceStatusReport": redisClient}
    try:
        ### Get Values for Status Report ###
        timeAndDate = datetime.datetime.now()
        timeCount = time.time()

        ### Base init ##timeAndDate#
        app = FastAPI()

        ### Error Handler load ###
        with open("../essentials/errorHandler.json", "r") as file:
            errorHandler = json.load(
                file)["services"][serviceName]

        ### CORS ###
        origins = ["*"]

        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"])

        ### Exception Handling Function ###
        @app.exception_handler(UnicornException)
        async def unicorn_exception_handler(request: Request, exc: UnicornException):
            return JSONResponse(
                status_code=exc.statusCode,
                content={"errorContext": exc.errorContext,
                         "message": errorHandler[exc.internalErrorCode]})

        ### Send Services Status Report ###
        servicesStatusReport.send(serviceName, databases, None, None, "GroundInit", timeAndDate, time.time() - timeCount, 0)
        return app, UnicornException, databases
    except Exception as e:
        ### Send Services Status Report (for error) ###
        servicesStatusReport.send(serviceName, databases, "100", e, "GroundInit", timeAndDate, time.time() - timeCount, 4)
        print(e)