from datetime import datetime

# Define function to convert str time to datetime time.
def convert_time(t):
    
    try:
        dt_t = datetime.strptime(t[:-6], "%Y-%m-%dT%H:%M:%S")
        
        if dt_t > datetime.now():
            td = dt_t - datetime.now()
            
            if td.seconds < 60:
                # Return "Arr" if bus arriving within one minute
                return "Arr"
            else:
                # Return time of arrival in minutes
                return round(td.seconds/60)
        else:
            return ""
    
    except:
        return ""