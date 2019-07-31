import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import *
import scipy.stats as stats
import math

import warnings
warnings.filterwarnings('ignore')


def plot_alignment_result_density(alignment_results, to_edit_width, to_edit_step, file_name, file_path):
    plt.figure(figsize=(20, 10))
    for (count, single_alignment_result) in enumerate(alignment_results):
        if len(alignment_results) != 1:
            plt.subplot(math.ceil(len(alignment_results) / 2), 2, count+1)
        plot_density_detail(count+1, single_alignment_result, to_edit_step, to_edit_width, file_name[count])

    name = "distribution {}width{}.png".format(to_edit_step, to_edit_width)

    if file_path is not None:
        plt.savefig(os.path.join(file_path, name))
    else:
        plt.savefig(name)


def plot_density_detail(count, alignment_result, to_edit_step, to_edit_width, file_name):
    output_list = alignment_result.window(
        width=to_edit_width,
        step=to_edit_step)
    i_list, distance_list, substitution_list, deletion_list, insertion_list = \
        _prepare_plot(output_list, to_edit_step)

    mean_distance = np.mean(distance_list)
    sns.set_style("ticks")
    w, p = stats.shapiro(distance_list)  # we will reject the hypothesis if p <0.05. X is not normal distribution.
    # plt.figure(figsize=(8, 4), dpi=100)
    sns.distplot(distance_list, hist=True, kde=True, rug=True, fit=norm,
                 kde_kws={"color": "lightcoral", "lw": 1.5, 'linestyle': '--'},
                 rug_kws={'color': 'lightcoral', 'alpha': 1, 'lw': 2, }, label='distance')

    plt.axvline(mean_distance, color='lightcoral', linestyle=":", alpha=2)
    plt.text(mean_distance + 2, 0.012, 'distance mean: %.1fcm' % (min(distance_list)), color='indianred')

    plt.text(min(distance_list), 0.012, 'min: %.1fcm' % (min(distance_list)), color='blue')

    plt.text(max(distance_list), 0.012, 'max: %.1fcm' % (max(distance_list)), color='blue')

    plt.annotate(s='We are using The Shapiro-Wilk test'.format(p), xy=(max(distance_list) - min(distance_list), 0.03))
    plt.annotate(s='p_value{} '.format(p), xy=(max(distance_list) - min(distance_list), 0.025))
    plt.annotate(s='w{} '.format(w), xy=(max(distance_list) - min(distance_list), 0.02))
    # plt.annotate(
    # s='the closer of w to 1,\n the better the normal distribution fits', xy=(max(distance_list) - 3, 0.04))
    if p > 0.05:
        plt.annotate(s='it is a normal distribution', xy=(max(distance_list) - min(distance_list), 0.015))
    plt.grid(linestyle='--')
    plt.xlabel("{} \n step{} width{}".format(file_name, to_edit_step, to_edit_width))
    plt.ylabel("distance")
    plt.legend()
    plt.title("{}distance per step".format(count),
              fontsize='medium')


def plot_distance_detail(count, alignment_result, to_edit_width, to_edit_step, file_name):
    print('count', count)
    output_list = alignment_result.window(
        width=to_edit_width,
        step=to_edit_step)
    i_list, distance_list, substitution_list, deletion_list, insertion_list = \
        _prepare_plot(output_list, to_edit_step)

    plt.plot(i_list, distance_list, 'r--', label='distance')
    plt.plot(i_list, substitution_list, 'b--', label='substitution')
    plt.plot(i_list, deletion_list, 'g--', label='deletion')
    plt.plot(i_list, insertion_list, 'm--', label='insertion')
    plt.plot(i_list, distance_list, 'ro')
    plt.xlabel("{} \n step{} width{}".format(file_name, to_edit_step, to_edit_width))
    plt.ylabel("distance")
    plt.legend()
    plt.title("{} distance per step".format(count),
              fontsize='medium')


def plot_alignment_result(alignment_results, to_edit_width, to_edit_step, file_name, file_path):
    plt.figure(figsize=(20, 10))
    for (count, single_alignment_result) in enumerate(alignment_results):

        if len(alignment_results) != 1:
            plt.subplot(math.ceil(len(alignment_results) / 2), 2, count+1)

        plot_distance_detail(count+1, single_alignment_result, to_edit_width, to_edit_step, file_name[count])

    name = "{}distance {}width{}.png".format('distance_plot', to_edit_step, to_edit_width)
    if file_path is not None:
        plt.savefig(os.path.join(file_path, name))
    else:
        plt.savefig(name)


def _prepare_plot(output_list, step):
    distance_list = list()
    substitution_list = list()
    deletion_list = list()
    insertion_list = list()
    i_list = list(range(0, len(output_list)*step, step))
    for i in output_list:
        distance, substitution, insertion, deletion = i.calculate_three_kinds_of_distance()
        distance_list.append(distance)
        substitution_list.append(substitution)
        deletion_list.append(deletion)
        insertion_list.append(insertion)

    return i_list, distance_list, substitution_list, deletion_list, insertion_list
