print("bob")
from functions import *
from envs import *
from pprint import pprint
import os


ips_doc = "ips.txt"

ips_string = read_file_to_string(ips_doc)
ips_list = get_ip(ips_string)
pprint(ips_list)
for ip in ips_list:
    print(ip)
    net_connect = make_connection(ip, username, password, "linux")
    output = send_command(net_connect, "ll")
    print(output)
    output = send_command(net_connect, "kubectl get nodes")
    print(output)
    to_doc_w(f"{ip}.text", ip)
