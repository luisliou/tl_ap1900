import hashlib
import requests
import re

from enum import Enum


class TpLink1900LoginType(Enum):
    SYN = 0
    ASYNC = 1
    TDDP_INSTRUCT = 0
    TDDP_WRITE = 1
    TDDP_READ = 2
    TDDP_UPLOAD = 3
    TDDP_DOWNLOAD = 4
    TDDP_RESET = 5
    TDDP_REBOOT = 6
    TDDP_AUTH = 7
    TDDP_GETPEERMAC = 8
    TDDP_CONFIG = 9
    TDDP_CHGPWD = 10
    TDDP_LOGOUT = 11
    TDDP_CONFLICT = 12
    TDDP_FACTINIT = 13
    TDDP_VERSION = 14
    EXTEND_INFO = 16


class TpLink1900State(Enum):
    INITED = 0
    LOGIN_FAILED = 1
    LOGIN_SUCCEED = 2


class LoginTpLink1900(object):
    INPUT1 = "RDpbLfCPsJZ7fiv"
    INPUT3 = "yLwVl0zKqws7LgKPRQ84Mdt708T1qQ3Ha7xv3H7NyU84p21BriUWBU43odz3iP4rBL3cD02KZciXTysVXiV8ngg6vL48rPJyAUw0HurW20xqxv9aYb4M9wK1Ae0wlro510qXeU07kV57fQMc8L6aLgMLwygtc0F10a0Dg70TOoouyFhdysuRMO51yY5ZlOZZLEal1h0t9YQW0Ko7oBwmCAHoic4HYbUyVeU3sfQ1xtXcPcf1aT303wAQhv66qzW"
    URL_STRING = "http://{0}/?code={1}&async=1&id={2}"

    def __init__(self):
        self.user = ""
        self.password = ""
        self.ip = ""
        self.token = ""
        self.state = TpLink1900State.INITED

    @staticmethod
    def __encrypt_pwd__(password, key, dictionary):
        len1 = len(key)
        len2 = len(password)
        len_dict = len(dictionary)
        output = ''
        if len1 > len2:
            length = len1
        else:
            length = len2
        index = 0
        while index < length:
            cl = 187
            cr = 187
            if index >= len1:
                cr = ord(password[index])
            elif index >= len2:
                cl = ord(key[index])
            else:
                cl = ord(key[index])
                cr = ord(password[index])
            index += 1
            output = output + chr(ord(dictionary[cl ^ cr]) % len_dict)
        return output

    def __get_token__(self):
        encoded_pass = self.__encrypt_pwd__(self.password, self.INPUT1, self.INPUT3)
        full_str = self.user + ';' + encoded_pass
        code = hashlib.md5(full_str.encode(encoding="UTF-8"))
        return code.hexdigest()

    def login(self, ip, user, password):
        self.ip = ip
        self.user = user
        self.password = password
        remote_token = self.__get_remote_token__(ip)
        token = self.__encrypt_pwd__(self.__get_token__(), remote_token[0], remote_token[1])
        log_req_url = self.URL_STRING.format(ip, TpLink1900LoginType.TDDP_AUTH, token)
        log_req = requests.post(log_req_url)
        if log_req.status_code == 200:
            self.token = token
            self.state = TpLink1900State.LOGIN_SUCCEED
        else:
            self.token = ""
            self.state = TpLink1900State.LOGIN_FAILED

    def __get_remote_token__(self, ip):
        ret = []
        req = requests.post(self.URL_STRING.format(ip, TpLink1900LoginType.TDDP_READ.value, ""))
        response_list = req.text.splitlines()
        if len(response_list) < 6:
            exit(-1)
        ret.append(response_list[3])
        ret.append(response_list[4])
        return ret

    def get_state(self, read_string):
        if self.state != TpLink1900State.LOGIN_SUCCEED:
            return
        req_url = self.URL_STRING.format(self.ip, TpLink1900LoginType.TDDP_READ.value, self.token)
        response = requests.post(req_url, read_string)
        if response.status_code == 200:
            return response.text

    @staticmethod
    def __filter_mac__(all_info):
        if len(all_info) > 0:
            items = all_info.splitlines()
            return [item.replace("-", ":").split(" ")[2].upper() for item in items if re.search(r"[a-f0-9]{2}(-[a-f0-9]{2}){5}$", item) and
                    not re.search("00-00-00-00-00-00", item)]

    def get_active_mac(self):
        all_info = self.get_state("12#54#")
        mac = self.__filter_mac__(all_info)
        return mac
