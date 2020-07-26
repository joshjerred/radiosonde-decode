# Sounding Analysis - a tool to decode raw National Weather Service sounding data
# Use this PDF for reference https://meteor.geol.iastate.edu/classes/mt311/extras/Codul-TEMP.pdf

def daytime(timedata): # Decode the day/time codes
    day = int(timedata[0:2]) - 50 # The day of the month is calculated with the first two values minus 50
    time = int(timedata[2:4]) # The time is either 00 or 12, UTC time
    return day, time # Last digit (Normally 1) denotes wind data up to 100mb, not integrated into this

def tempdew(tempdata): # Decode the temp and dewpoint codes
    if tempdata == "/////": # If this data point level is below ground / data was not collected there will obviously be no data. It shows up as "/////" on the report
        return "nn"
    else:
        if int(tempdata[2]) % 2 == 0:
            tempdata = str(tempdata) # Converts the data into a string (Temporary?)
            temp = float(tempdata[0:2] + "." + tempdata[2:3]) # Calculate the temperature (Refer to the PDF)
        else:
            tempdata = str(tempdata) # Converts the data into a string (Temporary?)
            temp = -(float(tempdata[0:2] + "." + tempdata[2:3])) # Calculate the temperature (Refer to the PDF)
        dewpoint = float(tempdata[3] + "." + tempdata[4]) # This gets the Dewpoint Depression (Refer to PDF)
        if dewpoint < 5:   # When dewpoint depression is less than 5 you can just subtract from the temperature to get the dewpoint
            dewpoint = temp - dewpoint
        elif dewpoint > 5: # When the DD is above 5 it's in whole degrees and you need to subtract 50 from it
            dewpoint = temp - ((dewpoint * 10) - 50) # Multiply by 10 to get back into full degrees
        return temp, round(dewpoint, 1)

def wind(winddirspeed): # Decode the wind direction and speed, direction is in the resolution of 5 degrees
    if winddirspeed == "/////":
        return "nn"
    else:
        if winddirspeed[2] == "1": # If the windspeed => 100
            direction = int(winddirspeed[0:3]) - 1 # If the center digit is 1 the windspeed is equal to or over 100, this is not for resolution, subtract this from the direction
            speed = int(winddirspeed[2:5])
        elif winddirspeed[2] == "6": # If the center digit is 6 then the wind direction is 'xx5' and the wind speed is equal to or over 100
            direction = int(winddirspeed[0:3]) - 1 # Subtract 1 to change the direction from 'xx6' to 'xx5' as it should be 
            speed = int(winddirspeed[2:5]) - 500 # Subtract 500 from the last 3 digits to remove the 'xx5' direction resolution to get the wind speed
        else: # If the wind speed is less than 100
            direction = int(winddirspeed[0:3])
            speed = int(winddirspeed[3:5])
    return direction, speed

def surface(surfdata):
    if int(surfdata[2:5]) < 300:
        surfacepressure = int(surfdata[2:5]) + 1000
    else:
        surfacepressure =  int(surfdata[2:5])
    return surfacepressure

def getdata(tempdata, winddata):
    x = tempdew(tempdata)
    y = wind(winddata)
    z = x + y
    return z

def process(raw):
    info = {
        "datalevel": raw[0],
        "datetime": daytime(raw[1]),
        "stationident": raw[2],
    }

    data = {
        "surface": getdata(raw[4], raw[5]),
        "1000": getdata(raw[7], raw[8]),
        "925": getdata(raw[10], raw[11]),
        "850": getdata(raw[13], raw[14]),
        "700": getdata(raw[16], raw[17]),
        "500": getdata(raw[19], raw[20]),
        "400": getdata(raw[22], raw[23]),
        "300": getdata(raw[25], raw[26]),
        "250": getdata(raw[28], raw[29]),
        "200": getdata(raw[31], raw[32]),
        "150": getdata(raw[34], raw[35]),
        "100": getdata(raw[37], raw[38]),
    }

    temp = []
    dewpoint = []
    winddirection = []
    windspeed = []

    for key in data:
        temp.append(data[key][0])
        dewpoint.append(data[key][1])
        winddirection.append(data[key][2])
        windspeed.append(data[key][3])

    #print("Temperature at varying levels: " + str(temp))
    #print("Dew point at varying levels: " + str(dewpoint))
    return [temp, dewpoint]
#print("Temperature at varying levels: " temp)
#print("Temperature at varying levels: " temp)

