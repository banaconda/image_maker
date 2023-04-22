#!venv/bin/python3
import json
import sys
from volume import *
from image import *
from key import *
from guestfs_utils import command

if __name__ == '__main__':
    '''
    path
    username
    public_key
    mac
    vlan
    ip with mask
    gateway
    dns
    '''

    if sys.argv.__len__() < 2:
        print('Missing arguments')
        sys.exit(1)

    jsonString = sys.argv[1]
    data = json.loads(jsonString)

    path = data['path']
    username = data['username']
    public_key = data['public_key']
    mac = data['mac']
    vlan = data['vlan']
    ip = data['ip']
    gateway = data['gateway']
    dns = data['dns']
    cmdList = data['cmdList']

    print(json.dumps(data, indent=4))

    # open drive
    g = open_drive(path, 'qcow2')

    # mount
    mount_root(g)

    # install ssh server
    print(command(g, 'apt update -y'))
    print(command(g, 'apt autoremove -y openssh-server'))
    print(command(g, 'apt install -y openssh-server'))
    for cmd in cmdList:
        print(command(g, cmd))

    # create base user
    create_user(g, username, public_key)

    # create network
    create_netplan_yaml(g, 'eth0', mac, vlan, ip, gateway, dns)

    # close drive
    close_drive(g)

    sys.exit(0)
