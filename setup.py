import os

dir_path = os.path.dirname(os.path.realpath(__file__))
usertemp = raw_input("What temperature to switch relay? (*C) [24]")
maxtemp = float("{0:.2f}".format(float(usertemp)))
timetoread = int(raw_input("How long inbetween readings? (secs) [5]"))
timetowrite = int(raw_input("How long inbetween write to Thingspeak? (secs) [16]"))
thingspeakkey = "THINGSPEAK KEY HERE"

with open(dir_path + "/config.txt", "w") as configfile:
    configfile.write(str(maxtemp) + "\n" + str(timetoread) + "\n" + str(timetowrite) + "\n" + thingspeakkey) 
