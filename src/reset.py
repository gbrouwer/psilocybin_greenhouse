import os
import sys

#------------------------------------------------
if __name__ == '__main__':

    os.system('sudo killall VDCAssistant')
    os.system('sudo sysctl -w net.inet.udp.maxdgram=65536')

    #Reset all python ports using 3000
    cmd = 'lsof -i:3000 > ../data/messages/proc_3000'
    os.system(cmd)

    #Open file and read
    pids = []
    with open('../data/messages/proc_3000','r') as f:
        for line in f:
            elements = line.rstrip().split(' ')
            pid = elements[2]
            pids.append(pid)

    #Kill
    for pid in pids:
        cmd = 'kill -9 ' + pid
        print(cmd)
        os.system(cmd)

    #Reset all python ports using 6666
    cmd = 'lsof -i:6666 > ../data/messages/proc_6666'
    os.system(cmd)

    #Open file and read
    pids = []
    with open('../data/messages/proc_6666','r') as f:
        for line in f:
            elements = line.rstrip().split(' ')
            if (elements[0] == 'Python'):
                pid = elements[2]
                pids.append(pid)

    #Kill
    for pid in pids:
        cmd = 'kill -9 ' + pid
        print(cmd)
        os.system(cmd)