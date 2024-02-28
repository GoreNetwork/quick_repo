import os
import re
from ciscoconfparse import CiscoConfParse
from pprint import pprint

def find_child_text (file, text):
	all = []
	parse = CiscoConfParse(file)
	for obj in parse.find_objects(text):
		each_obj = []
		each_obj.append(obj.text)
		for each in obj.all_children:
			each_obj.append(each.text)
		all.append(each_obj)
	return all


# returns a list of IP addresses pulled from the input
def get_ip(input):
    return (
        re.findall(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', input))


def write_to_text_file(text, filename):
    with open(filename, 'w') as file:
        file.write(text)


# Directory containing the input files
input_dir = 'example_dir'

# TextFSM template file
template_file = 'textfsm_template.fsm'

# Output directory for parsed results
output_dir = 'parsed_results'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)


def get_after_first_space(text):
    # Find the index of the first space
    first_space_index = text.find(' ')
    # Get everything after the first space using slicing
    after_first_space = text[first_space_index + 1:]

    return after_first_space

def pull_subnet_data(data):
    subnets_data = []
    for line in data:
        if 'ip address' in line:
            ip_subnets = get_ip(line)
            subnets_data.append(ip_subnets)
    return subnets_data

def pull_interface_name(interface):
    for line in interface:
        if 'nterface' in line:
            line = line.split(' ')
            return line[-1]

def pull_description(interface):
    for line in interface:
        if 'description' in line:
            line = line.lstrip(' ')
            print (line)
            return (get_after_first_space(line))
    return "no description"

def pull_standby_data(interface):
    standbys = []
    for line in interface:
        if 'standby' in line:
            line = line.lstrip()
            line = line.split(' ')
            standby = line[1]
            if standby not in standbys:
                standbys.append(standby)
    return standbys


def pull_acls(interface):
    output = {"acl_in": "-",
              "acl_out": "-"}
    for line in interface:
        if 'access-group' in line:
            line = line.lstrip()
            line = line.split(' ')
            if line[-1] == 'in':
                output['acl_in']=line[-2]
            if line[-1] == 'out':
                output['acl_out']=line[-2]
    return output

def deal_with_interfaces(interfaces):
    all_interface_data = []
    for interface in interfaces:
        data = {
        'subnets' :  pull_subnet_data(interface),
        'interface_name' : pull_interface_name(interface),
        'description' : pull_description(interface),
        'standbys' : pull_standby_data(interface),
        'acls' : pull_acls(interface),
        }
        all_interface_data.append(data)
    return all_interface_data


def build_output(all_interface_data, filename):
    output = ''
    for each_interface in all_interface_data:
        if len(each_interface['standbys'])>1:
            print (filename, " Has multiple standbys on ", each_interface['interface_name'], "Please check this output")
        line = f"{each_interface['interface_name']},"
        subnet_lines = []
        if len(each_interface['subnets']) !=0:
            if len(each_interface['standbys'])==0:
                each_interface['standbys'] = ["-"]
            for each in each_interface['subnets']:
                tmp_line = line+f"{each[0]},-,{each[1]},{each_interface['description']},-,-,-,{each_interface['standbys'][0]},-,{each_interface['acls']['acl_in']}, {each_interface['acls']['acl_out']}\n"
                output = output+tmp_line
    output_file_name = f'{filename}_output.csv'
    write_to_text_file(output, output_file_name)

# Process each .txt file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.txt'):
        with open(os.path.join(input_dir, filename)) as f:
            data = f.read()
            data = data.split('\n')
            interfaces = find_child_text(data, 'nterface')
            # pprint (interfaces)
            all_interface_data = deal_with_interfaces(interfaces)
            build_output(all_interface_data, filename)
