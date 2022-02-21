import socket
import sys
import ipaddress
from threading import Thread
 
 
 
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
 
 
if ipaddress.ip_address(get_ip()) in ipaddress.ip_network('172.16.0.0/24'):
    network = ipaddress.IPv4Network('172.16.0.0/24')
elif ipaddress.ip_address(get_ip()) in ipaddress.ip_network('192.168.0.0/24'):
    network = ipaddress.IPv4Network('192.168.0.0/24')
elif ipaddress.ip_address(get_ip()) in ipaddress.ip_network('10.0.0.0/24'):
    network = ipaddress.IPv4Network('10.0.0.0/24')
else:
    print("Your machine is not in know private subnet!")
 
 
def scanner(port_start, port_stop):
 
    try:
        for address in list(network.hosts()):
            for port in range (port_start,port_stop):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                result = s.connect_ex((str(address), port))
                if result == 0:
                    if port == 80:
                        print (f"Port {port} on {address}: Open - HTTP")
                        s.close()
                    elif port == 443:
                        print (f"Port {port} on {address}: Open - HTTPS")
                        s.close()
                    else:
                        print (f"Port {port} on {address}: Open")
                        s.close()
                else:
                    #print (f"Port {port} on {address}: Closed")
                    s.close()
    except KeyboardInterrupt:
        print ("Ctrl+C, Exiting!")
        sys.exit()
    except socket.gaierror:
        print ("Could not resolve the hostname. Exiting!")
        sys.exit()
    except socket.error:
        print ("Could not connect to server. Exiting!")
        sys.exit()
 
 
start = 18
stop = 38
for i in range(100):
    t = Thread(target=scanner, args=(start, stop))
    start += 20
    stop += 20
    t.start()
