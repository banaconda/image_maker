import guestfs

from guestfs_utils import command


def open_drive(image_name, format):
    g = guestfs.GuestFS(python_return_dict=True)
    g.add_drive_opts(image_name,
                     format=format, readonly=0)
    g.set_network(True)
    g.launch()
    return g


def mount_root(g: guestfs.GuestFS):
    devices = g.list_devices()
    g.part_expand_gpt(devices[0])
    partitions = g.list_partitions()
    print(g.mount(partitions[0], "/"))


def create_user(g: guestfs.GuestFS, username, public_key):
    command(g, f'adduser --disabled-password --gecos "" {username}')
    command(g, f'usermod -aG sudo {username}')
    command(g, f'mkdir /home/{username}/.ssh')
    g.write(f'/home/{username}/.ssh/authorized_keys', public_key + '\n')
    print(command(g, f'ls -laR /home/{username}/'))
    command(g, f'chown -R {username}:{username} /home/{username}/.ssh')
    g.write(f'/etc/sudoers.d/nopassword',
            f'{username} ALL=(ALL) NOPASSWD:ALL')


def create_netplan_yaml(g, interface, mac_address, vlanId, ip_with_mask, gateway, nameserver):
    netplan_with_vlan_yaml = f'''
network:
    version: 2
    ethernets:
        {interface}:
            match:
                macaddress: {mac_address}
            set-name: {interface}
    vlans:
        {interface}.{vlanId}:
            id: {vlanId}
            link: {interface}
            addresses:
            - {ip_with_mask}
            dhcp4: false
            routes:
                - to: 0.0.0.0/0
                  via: {gateway}
            nameservers:
                addresses:
                - {nameserver}
'''

    netplan_without_vlan_yaml = f'''
network:
    version: 2
    ethernets:
        {interface}:
            match:
                macaddress: {mac_address}
            set-name: {interface}
            addresses:
            - {ip_with_mask}
            dhcp4: false
            routes:
                - to: 0.0.0.0/0
                  via: {gateway}
            nameservers:
                addresses:
                - {nameserver}
'''
    yaml_path = '/etc/netplan/50-cloud-init.yaml'

    if vlanId == 0:
        netplan_yaml = netplan_without_vlan_yaml
    else:
        netplan_yaml = netplan_with_vlan_yaml

    g.write(yaml_path, netplan_yaml)
    print(g.cat(yaml_path))


def close_drive(g):
    g.umount_all()
    g.close()
