import matplotlib.pyplot as plt


def plot_alignment_result(alignment_result, to_edit_width, to_edit_step, file_name):
    output_list = alignment_result.window(
        width=to_edit_width,
        step=to_edit_step)
    i_list, distance_list, substitution_list, deletion_list, insertion_list = \
        _prepare_plot(output_list, to_edit_step)

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
    plt.savefig("{}distance_per_step{}width{}.png".format(file_name, to_edit_step, to_edit_width))
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
