# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 15:49:26 2020

@author: Fredrik Möller


Functions separate and plot the raw metric scores produced by the different statistical functions
"""
import numpy as np
from typing import Tuple, List
import matplotlib.pyplot as plt

plt.style.use('seaborn')


def sigma_splitter(float_arr: List[float]) -> Tuple[List[List[int]], List[List[int]], List[List[int]]]:
    """
    separates the NCOF score into the 1-3 sigma outliers for the NCOF input
    @param float_arr: List[float]
    @return: inliers , pos_outliers , neg_outliers: List[List[int]], List[List[int]], List[List[int]]
    """
    "calculates the mean and std of the input score"
    mean = np.mean(float_arr)
    std = np.std(float_arr)

    "calculate which indexes that are input inliers"
    inliers = np.where(np.logical_and(float_arr >= mean - std, float_arr <= mean + std))
    inliers = inliers[0].tolist()

    "Calculates the 1-sigma postive  outliers"
    one_pos_sigma = np.where(np.logical_and(mean + std <= float_arr, float_arr < mean + 2 * std))
    "Calculates the 2-sigma postive  outliers"
    two_pos_sigma = np.where(np.logical_and(mean + 2 * std <= float_arr, float_arr < mean + 3 * std))
    "Calculates the 3-sigma postive  outliers"
    three_pos_sigma = np.where(mean + 3 * std <= float_arr)

    "Calculates the 1-sigma negative  outliers"
    one_neg_sigma = np.where(np.logical_and(mean - 2 * std < float_arr, float_arr <= mean - std))
    "Calculates the 2-sigma negative  outliers"
    two_neg_sigma = np.where(np.logical_and(mean - 3 * std < float_arr, float_arr <= mean - 2 * std))
    "Calculates the 3-sigma negative  outliers"
    three_neg_sigma = np.where(float_arr <= mean - 3 * std)

    "stores the positive outliers in a list of lists"
    pos_outliers = [one_pos_sigma[0],
                    two_pos_sigma[0],
                    three_pos_sigma[0]]
    pos_outliers = [l.tolist() for l in pos_outliers]

    "stores the negative outliers in a list of lists"
    neg_outliers = [one_neg_sigma[0],
                    two_neg_sigma[0],
                    three_neg_sigma[0]]
    neg_outliers = [l.tolist() for l in neg_outliers]

    "OUTPUT: list of indexes"
    "inliers: list of all inliers"
    "pos_outliers: list of 3 lists that corresponds to the 1,2,3 positive sigma outlers"
    "neg_outliers: list of 3 lists that corresponds to the 1,2,3 negative sigma outlers"
    return inliers, pos_outliers, neg_outliers


def sigma_splitter_TF_IDF(score: List[List[float]]) -> Tuple[List[List[List[int]]], List[List[List[int]]]]:
    """
    Additional step for sigma splitting for the TF-IDF method
    @param score: List[List[float]] , a matrix containinig the TF-IDF score for some senences
    @return:
    """
    inliers = []
    pos_outliers = []
    for lab in score:
        inliers_tmp, pos_outliers_tmp, _ = sigma_splitter(lab)
        inliers.append(inliers_tmp)
        pos_outliers.append(pos_outliers_tmp)
    "OUTPUT: list of indexes"
    "inliers: list of all inliers"
    "pos_outliers: list of lists that corresponds to the 1,2,3 positive sigma outlers for all classes"
    "neg_outliers: list of lists that corresponds to the 1,2,3 negative sigma outlers for all classes"
    return inliers, pos_outliers


def NCOF_plot(ncof_score, inliers: List[int], pos_outliers: List[List[List[int]]], neg_outliers: List[List[List[int]]],
              dot: int, class_perspective: int):
    """
    Plots the 1-3 sigma NCOF outliers
    @param ncof_score: get from 'calc_NCOF_from_raw_data' function
    @param inliers: List[int], list of indexes, get from NCOF_sigma_spliter
    @param pos_outliers: List[List[List[int]]] ,list of lists of lists of indexes, get from NCOF_sigma_spliter
    @param neg_outliers: List[List[List[int]]] ,list of lists of lists of indexes, get from NCOF_sigma_spliter
    @param dot: int, specifies the scatter dot size of the plot
    @param class_perspective: int, used during the plotting to specify the perspective of the plot
    @return:
    """

    fig, ax = plt.subplots()
    ax.set_ylabel('NCOF score')
    ax.set_xlabel('Dictionary index')
    ax.set_title(f"NCOF score in the persepctive of class: {class_perspective}")
    y = ncof_score[inliers]
    "plot outliers"
    plt.scatter(inliers, y, s=dot, c='k')
    colours = ['r', 'b', 'g']
    for i, out in enumerate(pos_outliers):
        plt.scatter(out, ncof_score[out], s=dot, c=colours[i], alpha=0.7)
    for i, out in enumerate(neg_outliers):
        plt.scatter(out, ncof_score[out], s=dot, c=colours[i], alpha=0.7)
    ax.legend(['Inliers', '1-sigma', '2-sigma', '3-sigma'])

    "Only the outliers version"
    "plot inliers"
    fig, ax = plt.subplots()
    ax.set_ylabel('NCOF score')
    ax.set_xlabel('Dictionary index')
    ax.set_title(f"NCOF score for outliers in the persepctive of class: {class_perspective}")
    "plot outliers"
    colours = ['r', 'b', 'g']
    for i, out in enumerate(pos_outliers):
        plt.scatter(out, ncof_score[out], s=dot, c=colours[i], alpha=0.7)
    for i, out in enumerate(neg_outliers):
        plt.scatter(out, ncof_score[out], s=dot, c=colours[i], alpha=0.7)
    ax.legend(['1-sigma', '2-sigma', '3-sigma'])


def TFIDF_plot(tfidf_score, inliers: List[int], outliers: List[List[List[int]]], dot: int, class_name: List[str]):
    """Plot the TF-IDF score for the specified input.
    plots seperated by what datapoints that are considered as inliers and 1-3 sigma outliers.

    @param tfidf_score: np array containing the TF-IDF score
    @param inliers: List[int], list of indexes that are considered inliers
    @param outliers: List[List[List[int]]], list of lists of indexes that are considered 1-3 sigma outliers
    @param dot: int ,scatter dot size
    @param class_name:  List[str], list containing the names of the classes the data comes from
    @return:
    """

    colours = ['r', 'b', 'g']
    fig, ax = plt.subplots()
    ax.set_ylabel(f"TF-IDF score")
    ax.set_xlabel(f"Dictionary index")
    ax.set_title(f" TF-IDF score for the {class_name} class")

    "Plot inliers"
    y = tfidf_score[inliers]
    plt.scatter(inliers, y, s=dot, c='k')
    "Plot outliers"
    for elm, c in zip(outliers, colours):
        y = tfidf_score[elm]
        plt.scatter(elm, y, s=dot, c=c)

        ax.legend(['Inliers', '1-sigma', '2-sigma', '3-sigma'])


def TFIDF_plot_outliers(tfidf_score, outliers: List[List[List[int]]], dot: int, from_class: List[str]):
    """
    Plot the TF-IDF score for the specified input.
    plots seperated by what datapoints that are considered as inliers and 1-3 sigma outliers.

    @param tfidf_score: np array containing the TF-IDF score
    @param outliers: List[List[List[int]]] , list of lists of lists of indexes that are considered 1-3 sigma outliers
    @param dot: int ,scatter dot size
    @param from_class: List[str], list containing the names of the classes the data comes from
    """

    colours = ['r', 'b', 'g']
    plt.figure()
    fig, ax = plt.subplots()
    ax.set_ylabel(f"TF-IDF score")
    ax.set_xlabel(f"Dictionary index")
    ax.set_title(f" TF-IDF outlier score for the {from_class} class")

    for elm, c in zip(outliers, colours):
        y = tfidf_score[elm]
        plt.scatter(elm, y, s=dot, c=c)
        ax.legend(['1-sigma', '2-sigma', '3-sigma'])
    plt.show()


def ind_2_txt(ind_list: List[List[int]], dictionary: dict) -> List[List[int]]:
    """
    Transform a list of integers to their text representation corresponding to the info in the dict
    @param ind_list: List[List[int]]
    @param dictionary: dict
    @return: words : List[List[str]]
    """
    "check if input list is a list of lists, else process as a single list"
    if any(isinstance(el, list) for el in ind_list):
        words = []
        for i, lst in enumerate(ind_list):
            txt_words = []

            for elm in lst:
                txt_words.append(dictionary[elm])
            words.append(txt_words)
    else:
        words = []
        for elm in ind_list:
            words.append(dictionary[elm])

    return words


def symmetric_set_difference(a: list, b: list) -> Tuple[list, list]:
    """
    Takes the symmetric set difference of two lists and presentes the results as two lists containing 'in a but not b' & 'in b but not a'
    @param a: list
    @param b: list
    @return: a_not_in_b, b_not_in_a: list, list
    """
    a_not_in_b = list(set(a).difference(b))
    b_not_in_a = list(set(b).difference(a))
    return a_not_in_b, b_not_in_a


def plot_histogram(data: List[float], bins: int = None, x_label: str = None, y_label: str = None, title: str = None,
                   legend: List[str] = None):
    """

    @param data: List[float]
    @param bins: int
    @param x_label: str
    @param y_label: str
    @param title: str
    @param legend: List[str]
    """
    if bins is None:
        bins = 500

    fig, ax = plt.subplots(1, 1)
    counts, _, _ = ax.hist(data, bins=bins)
    max_c = max(counts)
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    ax.set_title(title)
    ax.legend(legend)
    ax.set_ylim(0, max_c + 0.05 * max_c)
    plt.show()


def plot_merged_histogram(data: List[List[float]], bins: int = None, x_label: str = None, y_label: str = None,
                          title: str = None, legend: List[str] = None):
    """
    @param data: List[List[float]]
    @param bins: int
    @param x_label: str
    @param y_label: str
    @param title: str
    @param legend: List[str]
    """
    if bins is None:
        bins = 500

    fig, axes = plt.subplots(2, 1)
    counts_0, _, _ = axes[0].hist(data[0], bins=bins)
    counts_1, _, _ = axes[1].hist(data[1], bins=bins)

    max_0 = max(counts_0)
    max_1 = max(counts_1)

    axes[0].set_ylabel(y_label)
    axes[1].set_ylabel(y_label)
    axes[1].set_xlabel(x_label)
    axes[0].set_title(title)

    axes[0].legend([legend[0]])
    axes[1].legend([legend[1]])

    axes[0].set_xlim(0, 1)
    axes[1].set_xlim(0, 1)

    axes[0].set_ylim(0, max_0 + 0.05 * max_0)
    axes[1].set_ylim(0, max_1 + 0.05 * max_1)

    plt.show()


if __name__ == '__main__':
    pass
