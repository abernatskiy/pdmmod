#!/usr/bin/python


def addToDictList(dictionary,key,value):#TESTED
    if not key in dictionary.keys():
        dictionary[key]=[value]
    else:
        dictionary[key].append(value)
    return None

def addToDictNum(dictionary,key,value):
    if not key in dictionary.keys():
        dictionary[key]=value
    else:
        dictionary[key]+=value
    return None