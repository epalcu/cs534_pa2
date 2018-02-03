# Program Information:
# Make sure the nodes.txt is included in the same directory when you run
# this program.

import sys
import os
import re
from operator import itemgetter

###################################################################################
# Open the csv file of senders and receivers and return their corresponding lists #
###################################################################################
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

#############################################################
# Return recipient location in users list for current round #
#############################################################
def find_offset(user):
    index_i = ord(user[0]) - 97
    index_j = int(user[1])
    offset = (index_i*10) + index_j

    return offset

#############################################################
# Initialized a rnd_list dictionary                         #
#############################################################
def init_rnd_list(t):
    d = {}

    # # Obtain public nodes from nodes.txt file.
    # with open("nodes.txt") as f:
    #     lines = f.readlines()
    #     for line in lines[1:121]:
    #         id = line[0:64]
    #         d[id] = 0
    for i in t:
        for j in i:
            if j in d.keys():
                continue
            else:
                d[j] = 0

    return d


###########################################################################
# Fill the dictionary with usrs being keys, value is a list of tuples     #
# correpsonding to current round, first element, and a list of recipients #
# for that round, second element.                                         #
###########################################################################
def fill_dict(senders, receivers, dict):
    for rnd in range(0, len(senders)):
        targets = ['80c36eb1372ba2de9c3222748b9c2d5d0f59924a5f87da7e270c25758ae6da87',
                   '80294dd94243cfec921c56685040765ffccdcd89677e7040e16733ff645c7a0c',
                   '806ca14119a98ecf4160e8e4c4c0f49d6feae0b21076bd412b93e0ef9263caf9',
                   '80c0435f7fed4d24fb9bbf5915973a7d3cdec68f8ee66e935965238433c2cd45',
                   '804a74fecca6aabed86b2642ca5ddf91d03d1943a89c487a91a21bace9757ad3']

        rnd_list = init_rnd_list(receivers)
        for receiver in receivers[rnd]:
            num_messages = len(receivers[rnd])
            rnd_list[receiver] = (1/(num_messages*1.0))
        # Traverse list of senders for the current orund
        for sender in senders[rnd]:
            # Check that it is a valid sender
            if sender in targets:
                # Pop off sender if it sent for current round
                targets.pop(targets.index(sender))
                # If sender already in dictionary, simply append the current round list to its o_lists key
                if sender in dict.keys():
                    o_list = dict[sender]['o_lists']
                    o_list.append(rnd_list)
                # Else initialize a sender key with its initial o_list
                else:
                    dict[sender] = {'o_lists': [rnd_list], 'u_lists': []}
        # Traverse remaining senders that didn't send message in the round and add in round list to its u list
        for target in targets:
            # If sender already in dictionary, simply append the current round list to its u_lists key
            if target in dict.keys():
                u_list = dict[target]['u_lists']
                u_list.append(rnd_list)
            # Else initialize a sender key with its initial u_list
            else:
                dict[target] = {'o_lists': [], 'u_lists': [rnd_list]}
    return dict



def reduce_lists(dict, num_messages):
    reduced_dict = {}
    for key, value in dict.items():
        O = {}
        U = {}
        O_count = len(dict[key]['o_lists'])
        U_count = len(dict[key]['u_lists'])

        # Traverse O lists
        for list in range(0, len(dict[key]['o_lists'])):
            for recipient, prob in dict[key]['o_lists'][list].items():

                try:
                    if recipient in O.keys():
                        O[recipient] = O[recipient] + prob/O_count
                    else:
                        O[recipient] = prob/O_count
                except:
                    continue


        # Traverse U lists
        for list in range(0, len(dict[key]['u_lists'])):
            for recipient,prob in dict[key]['u_lists'][list].items():

                try:
                    if recipient in U.keys():
                        U[recipient] = U[recipient] + prob/U_count
                    else:
                        U[recipient] = prob/U_count
                except:
                    continue

        behavior_vector = probability_vector(O, U, num_messages)
        behavior_vector = sorted(behavior_vector, key=lambda x: x[1])

        reduced_dict[key] = behavior_vector
    return reduced_dict

def probability_vector(o, u, m):
    v = [0]*len(o)

    #for i in range(0, len(o)):
    #    v[i] = (o[i][0], round((m*o[i][1] - (m-1)*u[i][1]), 2))

    index = 0
    for (okey,ovalue), (ukey,uvalue) in zip(o.items(),u.items()):
        v[index] = (okey, round((m * ovalue - (m-1)*uvalue), 2))
        index += 1

    return v

########################
# Print out users, yo. #
########################
def print_dict(dict):
    for key, value in dict.items():
        friends = sorted(value, key=itemgetter(1))
        print "{0} --> {1}".format(key, friends[-2:])

if __name__ == "__main__":
    users = {}
    # Get the senders and receivers... booyah!!!
    senders, receivers = openFile(sys.argv[1])
    dict_of_targets = fill_dict(senders, receivers, users)
    reduced_dict = reduce_lists(dict_of_targets, len(receivers[0]))
    print_dict(reduced_dict)
