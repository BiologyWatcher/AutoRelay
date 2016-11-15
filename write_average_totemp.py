from time import sleep
import os

filename = "/home/pi/Documents/temp_temp.txt"
avgfile = open("/home/pi/Documents/last_ten_average_temp.txt","w")

def read():
    with open(filename,"r") as infile:
        try:
            data = [float(n) for n in infile.read().split()]
            lasttendata = data[(len(data)-10):len(data)]
            average = (sum(lasttendata))/10
            return average
    
        except (IOError, ValueError):
            destroy()
def loop():
    while True:
        if read() != None:
            avgfile.write("%0.2f\n" % read())
            avgfile.flush()
            os.fsync(avgfile)
            sleep(5)

def destroy():
    data = []
    avgfile.close()
    pass

if __name__ == '__main__':
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
