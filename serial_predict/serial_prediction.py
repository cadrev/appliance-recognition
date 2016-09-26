#!/usr/bin/env python

import serial
import socket
import time
import json
from   json import dumps

# load the necessary library 
from sklearn.externals import joblib
from sklearn.neighbors import KNeighborsClassifier

# Arbitrary com port value
COM_PORT = 'COM7'
ser      = serial.Serial(COM_PORT, baudrate=9600,timeout=1)

# load the pickle file of a particular model, in this the KNN model previously saved
neigh    = joblib.load('neigh.pkl') 

# Initialize TCP Sockets 
# We use TCP socket communication to deliver the predicted appliance on 
# a NodeJS webserver.
TCP_IP      = '127.0.0.1'
TCP_PORT    = 9000
BUFFER_SIZE = 1024
data        = ''

# Connect the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

# Loop Read on Serial
while 1:

    while(ser.inWaiting() > 0):
   	    
   	    # Read the data sent from the smart plug to the XBEE
        char  = ser.read(1024)
        data  = data + char 
        
        # Parse the data
        value = data.split(',')
        x     = np.array(value[2:8], dtype='|S4')
        y     = x.astype(np.float)
        
        # Get the features from the array
        res   = neigh.predict(y)
        
        # Place the power and prediction on the dictionary
        test = {
             "id1": {"pow": round(float(value[2]),4), "pred":int(res[0])},
             "id2": {"pow": round(0.0,4), "pred":0}, 
             "id3": {"pow": round(0.0,4), "pred":0}
        }

        data = ''  
        
        # convert the dictionary to a json dump
        val  = json.dumps(test)
        print val

        # send the json to a NodeJS server
        s.send(val)
        time.sleep(0.01)


# Close the socket connection
s.close()
