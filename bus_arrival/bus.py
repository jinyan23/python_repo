# Import modules
import pandas as pd

# Import custom functions
from get_arrivals import get_arrivals
from convert_time import convert_time



def bus(id):
    
    """
    This function will be called into the Python Dash dashboard and takes in an
    argument that is user input from the dashboard.
    
    Takes in an argument:
    1) Bus stop ID
    
    Returns a data frame containing the list of bus services at the queried bus
    stop.
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

if __name__ == "__main__":
    bus(id)