from functions import *
from pprint import pprint

ips_doc = "ips.txt"

ips_string = read_file_to_string(ips_doc)
ips_list = get_ip(ips_string)
pprint(ips_list)
for ip in ips_list:
    print(ip)
    # net_connect = make_connection(ip, 'admin', 'cisco')
    # output = send_command(net_connect, 'show ip int brief'))
    # print(output)
    to_doc_w(f"{ip}.text", ip)
