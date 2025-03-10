import re
import subprocess

def execute_traceroute(destination):

    try:
        trace = subprocess.run(["traceroute", "-I", destination], stdout=subprocess.PIPE)
        traceroute_output = trace.stdout.decode('utf-8')
        return traceroute_output

    except Exception as e:
        return "Error: " + str(e)

def parse_traceroute(traceroute_output):
    """
    Parses the raw traceroute output into a structured format.

    Args:
        traceroute_output (str): Raw output from the traceroute command

    Returns:
        list: A list of dictionaries, each containing information about a hop:
            - 'hop': The hop number (int)
            - 'ip': The IP address of the router (str or None if timeout)
            - 'hostname': The hostname of the router (str or None if same as ip)
            - 'rtt': List of round-trip times in ms (list of floats, None for timeouts)

    Example:
    ```
        [
            {
                'hop': 1,
                'ip': '172.21.160.1',
                'hostname': 'HELDMANBACK.mshome.net',
                'rtt': [0.334, 0.311, 0.302]
            },
            {
                'hop': 2,
                'ip': '10.103.29.254',
                'hostname': None,
                'rtt': [3.638, 3.630, 3.624]
            },
            {
                'hop': 3,
                'ip': None,  # For timeout/asterisk
                'hostname': None,
                'rtt': [None, None, None]
            }
        ]
    ```
    """

    address_info = []

    split = traceroute_output.split("\n")
    split = split[1:-1]

    counter = 0

    while counter < len(split):
        parts = split[counter].split()

        if '*' in parts:
            hop_number = int(parts[0])
            address_info2 = {
                'hop': hop_number,
                'ip': None,
                'hostname': None,
                'rtt': [None, None, None]
            }
        else:
            if len(parts) < 8:
                counter += 1
                continue

            hop_number = int(parts[0])
            ip_address = parts[2]
            ip_address = re.sub(r"\(|\)", "", ip_address)
            hostname = parts[1]
            rtt = [float(parts[3]), float(parts[5]), float(parts[7])]
            address_info2 = {
                'hop': hop_number,
                'ip': ip_address,
                'hostname': hostname,
                'rtt': rtt
            }
        address_info.append(address_info2)
        counter += 1

    # Create a list to hold the formatted strings
    formatted_info = ["["]

    # Manually format the address_info list
    for i, info in enumerate(address_info):
        rtt_str = f"[{', '.join(map(str, info['rtt']))}]"
        ip_str = f"'{info['ip']}'" if info['ip'] is not None else "None"
        hostname_str = f"'{info['hostname']}'" if info['hostname'] is not None else "None"
        formatted_info.append(f"    {{\n        'hop': {info['hop']},\n        'ip': {ip_str},\n        'hostname': {hostname_str},\n        'rtt': {rtt_str}\n    }}")
        if i < len(address_info) - 1:
            formatted_info[-1] += ","

    # Add the closing bracket for the list
    formatted_info.append("]")

    # Join the list into a single string with new lines
    return "\n".join(formatted_info)

# Call execute_traceroute and parse_traceroute
traceroute_output = execute_traceroute("10.103.0.54")
address_info = parse_traceroute(traceroute_output)
print(address_info)