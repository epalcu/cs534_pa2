# Program Description

# Put this program into the directory in which you wish to pull rounds.
# This program will create 120 files, one for each public node - given
# the name of the node appended with '.txt', and write all round
# information for that node to the file.
#
# This program will run for exactly 10 hours.

import socket
import threading
import time
import sys
import os
import re
from operator import itemgetter

def thread_function(node,curTime):
    
    id = node[0:64]
    ip = node[65:77]
    port = int(node[78:])

    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    add = (ip,port)
    socket1.connect(add)

    fname = id + ".txt"
    f = open(fname, "w")

    type = ""
    m = ""
    while True:
        data = socket1.recv(1).decode("utf-8")
        if(data == '\n'):
            if(m in ("OFFER","ACK")):
                m = str(time.time()) + " " + m + " "
            else:
                f.write(m + '\n')
                f.flush()
                m = ""
        else:
            m += data


if __name__ == "__main__":
    
    nodes = []

    # Obtain public nodes from nodes.txt file.
    with open("nodes.txt") as f:
        lines = f.readlines()
        for line in lines[1:121]:
            nodes.append(line.rstrip())

    curTime = time.time()
    for node in nodes:
        t = threading.Thread(target=thread_function,args=(node,curTime))
        t.daemon = True
        t.start()

    while time.time() - curTime < 43200:
        curTime = curTime

