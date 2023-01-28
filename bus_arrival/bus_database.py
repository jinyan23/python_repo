import json
import httplib2 as http 
from urllib.parse import urlparse

import pandas as pd

# API Call Settings
uri = "http://datamall2.mytransport.sg/"
with open("../../python_repo_doc/bus_arrival_doc/LTA_AccountKey") as k: # type: ignore
    key = k.readlines()

method = "GET"
body = ""
h = http.Http()
headers = {"AccountKey": key[0],
           "accept": "application/json"}


# Define function to retrieve all available bus stops in Singapore
def bus_database():
    
    # Create empty list to hold list of bus stops
    bsObj = list()
    
    # Each API call only returns 500 records.
    # Total number of bus stops in Singapore slightly > 5,000
    for i in range(0, 5500, 500):
        
        # Iterating through each call of 500 records.
        target = urlparse(uri + "ltaodataservice/BusStops?$skip=" + str(i))
        
        response, content = h.request(
            target.geturl(),
            method,
            body,
            headers
            )
        
        bsObj.extend(json.loads(content)["value"])
    
    # Build all the responses into a dataframe for output    
    bs_df = pd.DataFrame({"busStopCode": [i["BusStopCode"] for i in bsObj],
                          "roadName": [i["RoadName"] for i in bsObj],
                          "description": [i["Description"] for i in bsObj],
                          "latitude": [i["Latitude"] for i in bsObj],
                          "longitude": [i["Longitude"] for i in bsObj]})


    # Retrieve list of all service routes in Singapore
    # Contains arrival sequence of bus at bus stop

    brObj = list()

    for i in range(0, 27000, 500):
        
        target = urlparse(uri + "ltaodataservice/BusRoutes?$skip=" + str(i))
        
        response, content = h.request(
            target.geturl(),
            method,
            body,
            headers)

        brObj.extend(json.loads(content)["value"])

    br_df = pd.DataFrame({"serviceNo": [i["ServiceNo"] for i in brObj],
                        "busStopCode": [i["BusStopCode"] for i in brObj],
                        "busStopSeq": [i["StopSequence"] for i in brObj],
                        "direction": [i["Direction"] for i in brObj]})

    bus_db = br_df.merge(bs_df, on="busStopCode")
    
    
    return bus_db


if __name__ == "__main__":
    bus_database()