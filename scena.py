import math
import time
import telnetlib

with open('COORD1.txt', 'r') as f:
    my_string = f.readlines()
    for i in my_string:
        telnet = telnetlib.Telnet('192.168.1.159')
        telnet.write(i.encode())
        print(i)
        time.sleep(2)



