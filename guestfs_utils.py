from guestfs import GuestFS


def command(g: GuestFS, cmd_string: str):
    return g.command(cmd_string.split(' '))
