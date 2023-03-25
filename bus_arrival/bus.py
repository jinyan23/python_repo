# Import modules
import pandas as pd
import math

# Import custom functions
from get_arrivals import get_arrivals
from convert_time import convert_time
from bus_database import bus_database

bus_db = bus_database()

def bus(id):
    
    """
    Description
    -----------
    Function will be called into the Python Dash dashboard and takes in an
    argument that is user input from the dashboard.
    
    Parameters
    ----------
    id : integer of bus stop code

    Returns
    -------
    Data frame containing the list of bus services at the queried bus stop.
    """
    
    # Check if bus stop ID is valid.
    if not id.isdigit() or len(id) != 5:
        err_message = "Invalid bus stop ID."
    elif not id in (["12345", "23456"]):
        err_message = "Bus stop does not exist."
    else:
        err_message = None
    
    # Get bus arrival timings from specific bus stop code.
    jsonObj = get_arrivals(bus_stop_code = id)

    # Extract bus arrival timings from JSON object.
    service_num = [bus["ServiceNo"] for bus in jsonObj["Services"]]
    nb_1_arr = [bus["NextBus"]["EstimatedArrival"] for bus in jsonObj["Services"]]
    nb_2_arr = [bus["NextBus2"]["EstimatedArrival"] for bus in jsonObj["Services"]]
    nb_3_arr = [bus["NextBus3"]["EstimatedArrival"] for bus in jsonObj["Services"]]

    # Convert bus arrival timings to minutes from now.
    nb_1_min = [convert_time(bt) for bt in nb_1_arr]
    nb_2_min = [convert_time(bt) for bt in nb_2_arr]
    nb_3_min = [convert_time(bt) for bt in nb_3_arr]

    bus_list = pd.DataFrame({"Service Number": service_num,
                            "Next Bus": nb_1_min,
                            "Next Bus 2": nb_2_min,
                            "Next Bus 3": nb_3_min})

    # Print out data frame coming bus arrival timings in minutes
    # print("After Conversion:\n", bus_list.sort_values(by="Service Number"))
    
    return bus_list, err_message


# Bus routes database (return list of bus stops in direction 1)
def route(service_num, direction=1):
     
    """    
    Description
    -----------
    Functions takes in bus service number and returns a list of bus stops 
    serviced by the queried bus.
    
    Parameters
    ----------
    service_num : string of bus service number
        Requires a string input as a bus service number. Some buses in Singapore
        have alphabet suffixes at the tail of the service number. 
    direction : integer
        Buses ply in two directions, sometimes using different roads. 
    
    Returns
    -------
    Data frame containing the list of bus stops serviced by the queried bus 
    service number.
    """
    
    service_num_mask = bus_db["serviceNo"] == str(service_num)
    direction_mask = bus_db["direction"] == direction
    
    stop_df = bus_db[service_num_mask & direction_mask]
    
    # Arrange bus stops in sequence of bus arrival
    stop_df.sort_values(by="busStopSeq", ascending=True, inplace=True)
        
    return stop_df


def nearest(geo_location):
    
    """    
    Description
    -----------
    Functions calculates the distance between current location and bus stops
    near the current location.
    
    Parameters
    ----------
    NA (at the moment)
    
    Returns
    -------
    Data frame containing the list of bus stops within 500m of current
    location
    """
    
    # Fix current location coordinates in.
    if geo_location==None:
        curr_loc = [1.310429, 103.854368]   # default location (Mustafa Centre)
    else:
        curr_loc = [float(i) for i in geo_location.split(", ")]

    # Calculate bus stops' distances from current location.
    diff_lat = (curr_loc[0] - bus_db["latitude"])**2
    diff_lon = (curr_loc[1] - bus_db["longitude"])**2

    # Convert latitude/longitude difference into distance in metrics system
    bus_db["distance"] = [math.sqrt(x + y)*111 for x, y in zip(diff_lat, diff_lon)]

    # Subset bus stops which are 500 metres away from current location.
    bs_output = bus_db[bus_db["distance"] < 0.5]
    bs_output = (bs_output.drop(["serviceNo", "busStopSeq", "direction", 
                                "latitude", "longitude", "distance"], axis=1)
                          .drop_duplicates("busStopCode")
                          .rename(columns={"busStopCode": "Bus Stop Code",
                                           "roadName": "Road Name",
                                           "description": "Description"})
                          .sort_values("Description"))
    
    return bs_output



if __name__ == "__main__":
    bus(id)