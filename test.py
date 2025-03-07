from amazing_trace import execute_traceroute, parse_traceroute
import subprocess

address_info = [

]

addresses = execute_traceroute("google.com")
print(addresses)
split = addresses.split("\n")
split = split[1:-1]

counter = 0

while counter < len(split):
    hop_number = split[counter].split()[0]
    ip_address = split[counter].split()[2]
    hostname = split[counter].split()[1]
    rtt = [split[counter].split()[3], split[0].split()[5], split[0].split()[7]]
    address_info2 = ({
        'hop': hop_number,
        'ip': ip_address,
        'hostname': hostname,
        'rtt': rtt
    })
    address_info.append(address_info2)
    counter += 1


print(address_info)