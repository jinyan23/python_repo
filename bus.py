import json
import urllib
import httplib2 as http 
from urllib.parse import urlparse
import os
import pandas as pd

from datetime import datetime

# Read in Token
with open("../python_repo_doc/bus_arrival_doc/LTA_AccountKey") as k:
    key = k.readlines()

# LTA Datamall API
headers = {"AccountKey": key[0],
           "accept": "application/json"}

uri = "http://datamall2.mytransport.sg/"

# Define GET methods
method = "GET"
body = ""
h = http.Http()


# Define function to retrieve bus arrivals from LTA Datamall
def get_arrivals(bus_stop_code):
    
    path = "ltaodataservice/BusArrivalv2?BusStopCode=" + str(bus_stop_code)

    target = urlparse(uri + path)  
    
    reponse, content = h.request(
        target.geturl(),
        method,
        body,
        headers
    )

    jsonObj = json.loads(content)
    
    return jsonObj


# Get bus arrival timings from specific bus stop code.
jsonObj = get_arrivals(bus_stop_code = "05013")     # To request user input here

# Filter out bus arrivals from JSON object.
service_num = [bus["ServiceNo"] for bus in jsonObj["Services"]]
service_num_1 = [bus["NextBus"]["EstimatedArrival"] for bus in jsonObj["Services"]]
service_num_2 = [bus["NextBus2"]["EstimatedArrival"] for bus in jsonObj["Services"]]
service_num_3 = [bus["NextBus3"]["EstimatedArrival"] for bus in jsonObj["Services"]]

bus_list = pd.DataFrame({"Service Number": service_num,
                         "Next Bus": service_num_1,
                         "Next Bus 2": service_num_2,
                         "Next Bus 3": service_num_3})

# Define function to convert str time to datetime time.
def convert_time(t):
    
    try:
        dt_t = datetime.strptime(t[:-6], "%Y-%m-%dT%H:%M:%S")
        
        if dt_t > datetime.now():
            td = dt_t - datetime.now()
            
            if td.seconds < 60:
                return "Arr"
            else:
                return round(td.seconds/60)
        else:
            return ""
    
    except:
        return ""

bus_list["Next Bus"] = bus_list["Next Bus"].apply(convert_time)
bus_list["Next Bus 2"] = bus_list["Next Bus 2"].apply(convert_time)
bus_list["Next Bus 3"] = bus_list["Next Bus 3"].apply(convert_time)

# Print out data frame coming bus arrival timings in minutes
print("After Conversion:\n", bus_list.sort_values(by="Service Number"))