import subprocess 
import re
import time 
import datetime
import platform
import matplotlib.pyplot as plt
import numpy as np 

Signal = []
Date = []

def read_data_from_cmd():
    p = subprocess.Popen("netsh wlan show interfaces", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.read().decode('unicode_escape').strip()
    m = re.findall('SSID.*?ÿ:.*?([A-z 0-9 -]*).*?Signal.*?ÿ:.*?([0-9]*)%', out, re.DOTALL)
    
    p.communicate()
    print("Signal Strength : " + str(m[0][1]))
    return(m[0][1])

def Signal_Strength():
    while(True):
        print(read_data_from_cmd())
        '''Signal.append(read_data_from_cmd())
        localtime = time.localtime()
        result = time.strftime("%I:%M:%S %p", localtime)
        Date.append(result)
        time.sleep(1)'''


#read_data_from_cmd()
Signal_Strength()

