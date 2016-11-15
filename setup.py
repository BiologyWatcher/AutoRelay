import os

dir_path = os.path.dirname(os.path.realpath(__file__))
usertemp = raw_input("What temperature to switch relay? (*C) ")
maxtemp = float("{0:.2f}".format(float(usertemp)))
timetoread = int(raw_input("How long inbetween readings? (secs) "))
timetowrite = int(raw_input("How long inbetween write to Thingspeak? (secs) "))
#thingspeakkey = raw_input("Enter the Thingspeak API PostON key to write to ")
#thingspeakkey2 = raw_input("Enter the Thingspeak API PostOFF key to write to ")
#thingspeakkey3 = raw_input("Enter the Thingspeak API Temperature key to write to ")

with open(dir_path + "/config.txt", "w") as configfile:
    configfile.write(str(maxtemp) + "\n" + str(timetoread) + "\n" + str(timetowrite) + "\n") # + thingspeakkey + "\n" + thingspeakkey2 + "\n" + thingspeakkey3 + "\n")
