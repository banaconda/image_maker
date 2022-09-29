import subprocess
from shutil import copyfile


def create_image_volume(path, format, size):
    cmd = 'qemu-img create -f ' + format + ' ' + path + ' ' + size
    subprocess.run(cmd.split(' '))


def resize_image_volume(original_path, new_path, size):
    copyfile(original_path, new_path)
    cmd = 'qemu-img resize ' + new_path + ' ' + size
    subprocess.run(cmd.split(' '))
