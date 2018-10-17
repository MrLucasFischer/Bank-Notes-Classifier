#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 09:47:38 2018

@author: Lucas Fischer
@author: Joana Martins
"""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier, KernelDensity
from NaiveBayes import NaiveBayes


def standardize_data(data, column):
    """
        Standerdize the data from the given column forward

        Args:
            data   - The unstandardized data
            column - Column from which to start the standardarization

        Returns:
            The standardized data
    """

    mean = np.mean(data[:, column:], axis = 0)  #calculate the mean of all the columns from the given column forward
    std = np.std(data[:, column:])  #Calculate the standard deviation for all the columns from the given column forward
    data[:, column:] = (data[:, column:] - mean)/std #standerdize the data
    return data



def normalize_data(data, column):
    """
        Normalize the data from the given column forward

        Args:
            data   - The unormalized data
            column - Column from which to start the normalization

        Returns:
            The normalized data
    """

    min_data = np.min(data[:, column:]) #calculate the minimum for all the columns from the given column forward
    max_data = np.max(data[:, column:]) #calculate the maximum for all the columns from the given column forward
    data[:, column:] = (data[:, column:] - min_data) / (max_data - min_data)
    return data



def read_data_file(filename, delim):
    """ 
        Reads the data file and gets data separated by delimiter delim

        Args:
            filename - Name of the file to read
            delim    - Value delimiter of the given file
    """

    data = np.loadtxt(filename, delimiter = delim) # Load the data from file
    return data



def calculate_error(feats, x, y, train_ix, valid_ix, value, algorithm):
    """
        Calculates the cross validation error for the specified algorithm
        
        Args:
            feats     - Number of features
            x         - Matrix with all the feature values
            y         - Vector with the target values
            train_ix  - List of training indexes generated by the stratified k-fold
            valid_ix  - List of valid indexes generated by the stratified k-fold
            value     - C or K value to use in the specified algorithm
            algorithm - The algorithm to use

        Returns:
            The cross validation error for the specified algorithm
    """

    reg = LogisticRegression(C = value, tol=1e-10) if(algorithm == "logistic") else KNeighborsClassifier(n_neighbors = value)
    reg.fit(x[train_ix, :feats], y[train_ix])
    accuracy_training = reg.score(x[train_ix, :feats], y[train_ix])
    accuracy_validation = reg.score(x[valid_ix, :feats], y[valid_ix])
    return 1 - accuracy_training, 1 - accuracy_validation



def calculate_test_error(feats, x_train, y_train, x_test, y_test, value, algorithm):
    """
        Calculates the test error and class predictions, after training with the full training set
        
        Args:
            feats     - Number of features
            x_train   - Matrix with all the feature values for the training set
            y_train   - Vector with the target values for the training set
            x_test    - Matrix with all the feature values for the test set
            y_test    - Vector with the target values for the test set
            value     - C or K value to use in the specified algorithm
            algorithm - The algorithm to use

        Returns:
            The test error for the specified algorithm and a list with the class predictions predicted by that classifier after training
    """

    reg = LogisticRegression(C = value, tol=1e-10) if(algorithm == "logistic") else KNeighborsClassifier(n_neighbors = value)
    reg.fit(x_train[:, :feats], y_train[:])
    return (1 - reg.score(x_test[:, :feats], y_test[:]), reg.predict(x_test[:, :feats]))



def plot_crossVal_err(err_array, algorithm, if_log_c_axis = True, filename = 'cross_val_err_vs_c.png'):
    """ 
        Plots training and cross-validation errors vs C parameter
        
        Note:
            err_array[:,0] - C or K values (depending on the algorithm used)
            err_array[:,1] - training errors
            err_array[:,2] - validation errors

        Args:
            err_array     - Matrix previously explained
            algorithm     - The algorithm to plot
            if_log_c_axis - Boolean used to determine wheather to display the C axis in log scale
            filename      - The name of the image file to store the plot
    """

    plt.figure(figsize = (11, 8))
    font = {
    'weight' : 'regular',
    'size'   : 24}
    plt.rc('font', **font)
    if(algorithm == "logistic"):
        if (if_log_c_axis):
            plt.plot(np.log10(err_array[:,0]), err_array[:,1], "-r", label="training")
            plt.plot(np.log10(err_array[:,0]), err_array[:,2], "-b", label="validation")
            plt.xlabel('$\log_{10}(C)$')
        else:
            plt.plot(err_array[:,0], err_array[:,1], "-r", label="training")    
            plt.plot(err_array[:,0], err_array[:,2], "-b", label="validation")
            plt.xlabel('C')
    else:
        plt.plot(err_array[:,0], err_array[:, 1], "-r", label="training")
        plt.plot(err_array[:,0], err_array[:, 2], "-b", label="validation")
        if(algorithm == "knn"):
            plt.xlabel('k')
        else:
            plt.xlabel('band-with')
        
    plt.ylabel('error')
    plt.legend()
    
    plt.savefig(filename, dpi=300)
    plt.savefig(filename[0:-3]+"eps", dpi=300)
    plt.show()
    plt.close



def get_prior_and_kdes(x, y, bw):
    """
        Calculates the prior probability for each class and creates a list filled with KDE fitted for each feature

        Args:
            x  - Matrix with the feature values
            y  - Vector with the target values
            bw - Band-width value to use

        Returns:
            the prior probability for each class and creates a list filled with KDE fitted for each feature
    """

    return NaiveBayes().get_prior_and_kdes(x, y, bw, num_feats = 4)



def calculate_error_bayes(x_training, y_training, x_validation, y_validation, prior_kde_list):
    """
        Calculates the training and validation error of the Naive Bayes classifier

        Args:
            x_training     - Values of the training set
            y_training     - Labels of the training set
            x_validation   - Values of the validation set
            y_validation   - Labels of the validation set
            prior_kde_list - List containing the prior probability of class 0 and 1, aswell as a list with KDE's for all features (for both classes)

        Returns:
            The training and validation error
    """

    prior_class0 = prior_kde_list[0]
    prior_class1 = prior_kde_list[1]
    kde_list = prior_kde_list[2]
    nb = NaiveBayes()

    return nb.calculate_training_error(x_training, y_training, x_validation, y_validation, prior_class0, prior_class1, kde_list, num_feats = 4)



def calculate_test_error_bayes(x_test, y_test, x_full_train, y_full_train, best_bw):
    """
        Calculates the test error of the Naive Bayes classifier

        Args:
            x_test : Values of the test set
            y_test : Labels of the test set
            x_full_train : Values of the full set to use for training
            y_full_train : Labels of the full set to use for training

        Returns:
            The test error for the model and a list with the class predictions, after training with the full set and the best band-with found before
    """

    nb = NaiveBayes()
    prior_kde_list = nb.get_prior_and_kdes(x_full_train, y_full_train, best_bw, num_feats = 4)

    prior_class0 = prior_kde_list[0]
    prior_class1 = prior_kde_list[1]
    kde_list = prior_kde_list[2]
    
    return nb.calculate_test_error(x_test, y_test, x_full_train, y_full_train, best_bw, prior_class0, prior_class1, kde_list, num_feats = 4)



def calculate_mcnemar(predictions1, predictions2, ground_truth, test_error1, test_error2, classifier1, classifier2):
        """
            Method that actually computes the McNemar equation and outputs to the the standard-output which classifier is better

            Args:
                predictions1 - List with class predictions of classifier1
                predictions2 - List with class predictions of classifier2
                ground_truth - The ground-truth of this data-set
                test_error1  - The test error of classifier1, used to determine which classifier is better
                test_error2  - The test error of classifier2, used to determine which classifier is better
                classifier1  - The name of the first classifier
                classifier2  - The name of the second classifier
        """

        e01 = np.sum(np.logical_and(predictions1 != ground_truth, predictions2 == ground_truth))
        e10 = np.sum(np.logical_and(predictions2 != ground_truth, predictions1 == ground_truth))

        observed_value = ((abs(e01 - e10) - 1) ** 2 )/(e01 + e10)
        critical_point = 3.84 #Chi Squared with 95% confidence and 1 degree of freedom

        if(observed_value >= critical_point):

            if(test_error1 < test_error2):
                #They're significantly different, and classifier1 is better than classifier2
                print('Classifier "{}" and "{}" are significantly different, and {} is likely better than {}'.format(classifier1, classifier2, classifier1, classifier2)) 

            elif(test_error1 > test_error2):
                #They're significantly different, and classifier1 is better than classifier2
                print('Classifier {} and {} are significantly different, and {} is likely better than {}'.format(classifier1, classifier2, classifier2, classifier1)) 

            else:
                #They're significantly different but we don't know which one is better
                print("Classifier \"{}\" and \"{}\" are significantly different, but their score is the same".format(classifier1, classifier2)) 

        else:
            #They're not significantly different
            print('Classifier "{}" and "{}" are not significantly different'.format(classifier1, classifier2))




def get_metrics(predictions, ground_truth):
    """
        Method that calculates the precision and recall given the predictions and ground truth passed as arguments

        Args:
            predictions  - Class predictions that a classifier predicted
            ground_truth - A list with the actual classes of the values

        Returns:
            The precision and recall given the predictions and ground truth passed as arguments
    """

    #Transfrorm the arguments into numpy arrays
    predictions = np.array(predictions)
    ground_truth = np.array(ground_truth)

    #Examples
    # predictions  = [1, 0, 1, 1, 0]
    # ground_truth = [0, 0, 1, 1, 1]

    # predictions AND ground_truth     = [0, 0, 1, 1, 0] -> Gives us the true positives
    # predictions OR  ground_truth     = [1, 0, 1, 1, 0] -> This minus the true positives gives us the false positive (the first 1)
    # NOT predictions AND ground_truth = [0, 0, 0, 0, 1] -> Gives us the false negative

    true_positives = np.sum(np.logical_and(predictions, ground_truth))
    false_positives = np.sum(np.logical_or(predictions, ground_truth)) - true_positives
    false_negatives = np.sum(np.logical_and(np.logical_not(predictions), ground_truth))

    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)

    return precision, recall
