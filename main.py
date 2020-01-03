import tp1900
import sys

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("cmd [ip] [user] [password]")
        exit(-1)
    ip = sys.argv[1]
    user = sys.argv[2]
    password = sys.argv[3]
    tplink1900 = tp1900.LoginTpLink1900()
    tplink1900.login(ip, user, password)
    mac = tplink1900.get_active_mac()
    for one_mac in mac:
        print(one_mac)
