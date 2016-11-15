#setup
from time import sleep
import datetime
import RPi.GPIO as GPIO
import os
import httplib, urllib
GPIO.setmode(GPIO.BOARD)

readwait = open("/home/pi/RelayTemp/config.txt","r").readlines()[2]
wait = float(readwait)
key = open("/home/pi/RelayTemp/config.txt","r").readlines()[3].rstrip()
#postoffkey = open("/home/pi/RelayTemp/config.txt","r").readlines()[4].rstrip()
#temperaturekey = open("/home/pi/RelayTemp/config.txt","r").readlines()[5].rstrip()

#relay sig pin 11
GPIO.setup(11,GPIO.OUT)
GPIO.output(11,0)
log = open("/home/pi/RelayTemp/changelog.txt","w")
date_time = datetime.datetime.strftime(datetime.datetime.now(),"%d-%m-%Y %H:%M:%S")
log.write("Fan off at 00.00 *C " + date_time + "\n")
relaystate = 0
readfile = "/home/pi/Documents/last_ten_average_temp.txt"
xtemp = open("/home/pi/RelayTemp/config.txt","r").readlines()[0]
maxtemp = float(xtemp)
toread = open("/home/pi/RelayTemp/config.txt","r").readlines()[1]
timetoread = float(toread)
def read():
    with open(readfile,"r") as infile:
        try:
            data = [float(n) for n in infile.read().split()]
            latestdata = data[len(data)-1]
        
            return latestdata

        except (IOError, ValueError):
            destroy()
def loop(relaystate):
    while True:
        if read() != None:
#            print "Basing action on: %0.2f" % read()
            if read() >= maxtemp:
                if (relaystate == 0):
              
                    relaystate = 1
                    date_time = datetime.datetime.strftime(datetime.datetime.now(),"%d-%m-%Y %H:%M:%S")
                    log.write("Fan on  at " + str(read()) + " *C " + date_time + "\n")
                    log.flush()
                    os.fsync(log)
                    sleep(0.2)
                    poston()

                elif (relaystate == 1):
                    relaystate = 1
                    sleep(0.2)
            elif read() <= maxtemp:
                if (relaystate == 1):
                    relaystate = 0
                    date_time = datetime.datetime.strftime(datetime.datetime.now(),"%d-%m-%Y %H:%M:%S")
                    log.write("Fan off at " + str(read()) + " *C " + date_time + "\n")
                    log.flush()
                    os.fsync(log)
                    sleep(0.2)
                    postoff()


                elif (relaystate == 0):
                    relaystate = 0
                    sleep(0.2)
            GPIO.output(11,relaystate)       
            sleep(timetoread)
def poston():
    while True:
#        for line in open("/home/pi/RelayTemp/changelog.txt","r"):
#            last = line
#        temp = last[11:16]

        temp = 1
#        temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3 # Get Raspberry Pi CPU temp
        params = urllib.urlencode({'field1': temp, 'key':key })
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
#            print temp
#            print response.status, response.reason
            data = response.read()
            conn.close()

            os.system('/home/pi/pushbullet.sh "Fan turned ON"')

        except:
            print "connection failed"
        break    

def postoff():
    while True:
#        for line in open("/home/pi/RelayTemp/changelog.txt","r"):
#            last = line
#        temp = last[11:16]

        temp = 0
#        temp = int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3 # Get Raspberry Pi CPU temp
        params = urllib.urlencode({'field1': temp, 'key':key })
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
#            print temp
#            print response.status, response.reason
            data = response.read()
            conn.close()

            os.system('/home/pi/pushbullet.sh "Fan turned OFF"')

        except:
            print "connection failed"
        break

def destroy():
    data = []
    log.close()
    pass

if __name__ == '__main__':
    try:

        loop(relaystate)
    except KeyboardInterrupt:
        destroy()
