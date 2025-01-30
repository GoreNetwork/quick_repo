import re
import netmiko


def make_connection(ip, username, password):
    net_connect = netmiko.ConnectHandler(
        device_type="cisco_ios", ip=ip, username=username, password=password
    )
    return net_connect


def send_command(net_connect, command):
    return net_connect.send_command_expect(command)


def get_ip(input):
    return re.findall(
        r"(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)",
        input,
    )


def read_file_to_string(file_path):
    with open(file_path, "r") as file:
        return file.read()


def to_doc_w(file_name, varable):
    f = open(file_name, "w")
    f.write(varable)
    f.close()
