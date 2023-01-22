# Import modules
import pandas as pd

# Import custom functions
from get_arrivals import get_arrivals
from convert_time import convert_time

def main():
    
    # Get bus arrival timings from specific bus stop code.
    jsonObj = get_arrivals(bus_stop_code = "30089")     # To request user input here

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
    print("After Conversion:\n", bus_list.sort_values(by="Service Number"))

if __name__ == "__main__":
    main()