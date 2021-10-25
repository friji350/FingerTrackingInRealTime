import time
import telnetlib

for i in range(360):
    telnet = telnetlib.Telnet('192.168.43.62')
    s = f'A{i*1}'
    telnet.write(s.encode())
    print("A" + str(i))
    time.sleep(0.1)
s = f'A{0}'
telnet.write(s.encode())