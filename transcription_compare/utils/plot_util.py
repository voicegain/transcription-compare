import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import *
import scipy.stats as stats


import warnings
warnings.filterwarnings('ignore')


def t(distance_list, to_edit_step, to_edit_width):
    mean_distance = np.mean(distance_list)
    sns.set_style("ticks")
    w, p = stats.shapiro(distance_list)  # we will reject the hypothesis if p <0.05. X is not normal distribution.
    plt.figure(figsize=(8, 4), dpi=100)
    sns.distplot(distance_list, hist=True, kde=True, rug=True, fit=norm,
                 kde_kws={"color": "lightcoral", "lw": 1.5, 'linestyle': '--'},
                 rug_kws={'color': 'lightcoral', 'alpha': 1, 'lw': 2, }, label='distance')

    plt.axvline(mean_distance, color='lightcoral', linestyle=":", alpha=2)
    plt.text(mean_distance + 2, 0.012, 'distance mean: %.1fcm' % (mean_distance), color='indianred')
    plt.annotate(s='We are using The Shapiro-Wilk test'.format(p), xy=(max(distance_list) - 3, 0.055))
    plt.annotate(s='p_value{} '.format(p), xy=(max(distance_list) - 3, 0.05))
    plt.annotate(s='w{} '.format(w), xy=(max(distance_list) - 3, 0.045))
    plt.annotate(s='the closer of w to 1,\n the better the normal distribution fits', xy=(max(distance_list) - 3, 0.04))
    if p > 0.05:
        plt.annotate(s='it is a normal distribution', xy=(max(distance_list) - 3, 0.035))
    plt.grid(linestyle='--')
    plt.title("distribution_of_distance step{} width{}".format(to_edit_step, to_edit_width))
    plt.savefig("sample_data/distribution_of_distance")


def plot_alignment_result(alignment_result, to_edit_width, to_edit_step, file_name, file_path):
    output_list = alignment_result.window(
        width=to_edit_width,
        step=to_edit_step)
    i_list, distance_list, substitution_list, deletion_list, insertion_list = \
        _prepare_plot(output_list, to_edit_step)

    # data_frame = pd.DataFrame({'step': i_list, 'distance': distance_list,
    #                           'substitution': substitution_list,
    #                            'deletion': deletion_list,
    #                            'insertion': insertion_list})
    # data_frame = pd.DataFrame({'step': i_list, 'distance': distance_list})
    # data_frame.to_csv("distance.csv", index=False, sep=',')
    t(distance_list, to_edit_step, to_edit_width)

    print('distance', distance_list)
    print('deletion_list', deletion_list)
    print('insertion_list', insertion_list)
    plt.figure()
    plt.plot(i_list, distance_list, 'r--', label='distance')
    plt.plot(i_list, substitution_list, 'b--', label='substitution')
    plt.plot(i_list, deletion_list, 'g--', label='deletion')
    plt.plot(i_list, insertion_list, 'm--', label='insertion')
    plt.plot(i_list, distance_list, 'ro')
    plt.xlabel("step{} width{}".format(to_edit_step, to_edit_width))
    plt.ylabel("distance")
    plt.legend()
    plt.title("{}distance per step".format(file_name),
              fontsize='x-small')
    # font_size=['xx-small', 'x-small', 'small', 'medium', 'large','x-large', 'xx-large']
    name = "{}distance_per_step{}width{}.png".format(file_name, to_edit_step, to_edit_width)
    if file_path is not None:
        plt.savefig(os.path.join(file_path, name))
    else:
        plt.savefig(name)
    # plt.show()

    print('sum', sum(distance_list))
    print('substitution_list', sum(substitution_list))
    print('deletion_list', sum(deletion_list))
    print('insertion_list', sum(insertion_list))
    print('--------------------------')


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
