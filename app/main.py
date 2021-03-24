from fastapi.responses import JSONResponse
import json, os, sys, inspect, time, datetime
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from essentials import essential
from connectors import redisConnector

### FastAPI and Databases Init ###

serviceName = os.environ["serviceName"]
app, UnicornException, databases = essential.init(serviceName)

esClient = databases["elasticsearch"]
mongoDBClient = databases["mongoDB"]
redisXY = redisConnector.connect(XY) #Change XY to your name and the db number

### Service Functions ###

@app.get("/")
async def main():
    return JSONResponse(content={"message": "Hello World! I'm a meesage from a Template. A nice Template..."})



### GUIDE ### (You can delete this, if you make a API from the template)

#raise UnicornException(internalErrorCode="101", errorContext="I'm a Context", statusCode=500)
#---
#errorCode => The internal error code for the errorHandler and other system APIs 
#errorContext => The request from user and maby other data
#statusCode => HTTP error code like 404 or 500

#servicesStatusReport.send(serviceName, databases, errorCode, feedback, process, timeAndDate, timeCount, feedbackLevel)
#---
#serviceName => The name from the service
#databases => A list with elasticsearch-, mongodb-, redis-Client
#internalErrorCode => This is the internal error code for other APIs or to find faster error collections
#feedback => The errir or other. If only normal status report than make None as feedback
#process => What a function or process
#timeAndDate => Time and Date
#timeCount => How much time needed the process
#feedbackLevel => How critical is the report? 0=Normal, ..., 4=Down