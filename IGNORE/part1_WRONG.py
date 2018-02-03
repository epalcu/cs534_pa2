

import sys
import os
import re

def openFile(fname):
    
    senders = []
    receivers = []
    
    with open(fname) as fp:
        lines = fp.readlines()

        for line in lines:
            if line[0] == 'S':
                input = re.findall(r"(?<![@#])\b\w+(?:'\w+)?", line[1:])
                senders.append(input)
            else:
                input = re.findall(r"(?<![@#])\b\w+(?:'\w+)?", line[1:])
                receivers.append(input)
    return senders, receivers


def senderCheck(name):
    if(name[0] >= 'a' and name[0] <= 'z' and name[1] == '0'):
        return True
    else:
        return False


if __name__ == "__main__":

    # Get the senders and receivers... booyah!!!
    senders, receivers = openFile(sys.argv[1])

    target = ['a0','b0','c0','d0','e0','f0','g0','h0','i0','j0','k0','l0','m0','n0','o0','p0','q0','r0',
              's0','t0','u0','v0','w0','x0','y0','z0']
    
    # Two lists indexed as: [target][round][recipient]
    o_list = [[]]*26    # list representing o_i values (sender did send a message)
    u_list = [[]]*26    # list representing u_i values (sender didn't send a message)
    for i in range(26):
        o_list[i] = []
        u_list[i] = []

    # Go through each round
    for senders_rnd, receivers_rnd in zip(senders, receivers):

        o_i = [0]*260

        # Obtain the receiver list o_i
        for receiver in range(0, len(receivers_rnd)):
            index_i = ord(receivers_rnd[receiver][0]) - 97
            index_j = int(receivers_rnd[receiver][1])
            offset = index_i*10 + index_j
            o_i[offset] = 1/len(receivers_rnd)

        for t in target:
            index_i = ord(t[0]) - 97
            index_j = int(t[1])
            offset = index_i*10 + index_j
            
            if(t in senders_rnd):
                tmp = o_i[offset]
                o_i[offset] = 0
                o_list[index_i].append(o_i*1)
                o_i[offset] = tmp
                    
            else:
                u_list[index_i].append(o_i*1)

    #Analyze each target node
    for i in range(26):
        o_vector = [0]*260
        u_vector = [0]*260
        f_vector = [0]*260
        max1_index = 0
        max2_index = 0
    
        # Compute O
        a8 = 0
        for receiver in range(260):
            sum = 0
            for round in range(0,len(o_list[i])):

                if(receiver == 8 and i == 0):
                    a8 += o_list[i][round][receiver]
                
                
                sum += o_list[i][round][receiver]
            o_vector[receiver] = sum / len(o_list[i])
#o_vector[receiver] = sum


        # Compute U
        for receiver in range(260):
            sum = 0
            for round in range(0,len(u_list[i])):
                sum += u_list[i][round][receiver]
            u_vector[receiver] = sum / len(u_list[i])
#u_vector[receiver] = sum


        # Update O and U
        for j in range(260):
            o_vector[j] *= len(receivers_rnd)
            u_vector[j] *= (len(receivers_rnd) - 1)

        # Compute v
        for j in range(260):
            f_vector[j] = o_vector[j] - u_vector[j]
            
            # Keep track of top two probabilities
            if(j == 0):
                max1_index = j
                max2_index = j
            if(f_vector[j] < f_vector[max1_index] and
               f_vector[j] > f_vector[max2_index]):
                max2_index = j
            elif(f_vector[j] > f_vector[max1_index]):
                max2_index = max1_index
                max1_index = j

        char_val = int(max1_index/10) + 97
        int_val = max1_index%10
        r1 = chr(char_val) + str(int_val)

        char_val = int(max2_index/10) + 97
        int_val = max2_index%10
        r2 = chr(char_val) + str(int_val)

        print(target[i])
        print(r1, f_vector[max1_index])
        print(r2, f_vector[max2_index])
        print('')

#print(o_list[0][0])
#v_list = [[]]*26
#for i in range(26):
#v_list[i] = [0]*len(receivers)
























