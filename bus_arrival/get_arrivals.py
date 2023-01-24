import json
import urllib
import httplib2 as http 
from urllib.parse import urlparse

# Read in Token
with open("../../python_repo_doc/bus_arrival_doc/LTA_AccountKey") as k: # type: ignore
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