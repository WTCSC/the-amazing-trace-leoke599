from amazing_trace import execute_traceroute, parse_traceroute
import subprocess

addresses = execute_traceroute("google.com")
split = addresses.split("\n")
print(split)
for i in split:
    print(i)