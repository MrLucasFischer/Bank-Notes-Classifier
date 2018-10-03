#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 09:47:38 2018

@author: lucas
"""
import numpy as np
import matplotlib.pyplot as plt

def standerdize_data(data, column):
    """
        Standerdize the data from the given column forward
    """
    mean = np.mean(data[:, column:], axis = 0)  #calculate the mean of all the columns from the given column forward
    std = np.std(data[:, column:])  #Calculate the standard deviation for all the columns from the given column forward
    data[:, 1:] = (data[:, column:] - mean)/std #standerdize the data
    return data

def read_data_file(filename, delim):
    """ Reads the data file and gets data separated by delimiter delim """
    """ input: filename to read (filename), delimeter (delim) """
    """ ouput: data """
    # Load the data from file
    data = np.loadtxt(filename,delimiter=delim)
    return data
