#!/usr/bin/python3
import shutil
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

    if sys.argv.__len__() < 9:
        print('Missing arguments')
        sys.exit(1)

    path = sys.argv[1]
    username = sys.argv[2]
    public_key = sys.argv[3]
    mac = sys.argv[4]
    vlan = sys.argv[5]
    ip = sys.argv[6]
    gateway = sys.argv[7]
    dns = sys.argv[8]

    for arg in sys.argv:
        print(arg)

    # open drive
    g = open_drive(path, 'qcow2')

    # mount
    mount_root(g)

    # install ssh server
    print(command(g, 'apt update -y'))
    print(command(g, 'apt autoremove -y openssh-server'))
    print(command(g, 'apt install -y openssh-server'))

    # create base user
    create_user(g, username, public_key)

    # create network
    create_netplan_yaml(g, 'eth0', mac, vlan, ip, gateway, dns)

    # close drive
    close_drive(g)
