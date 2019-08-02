
from transcription_compare.levenshtein_distance_calculator import UKKLevenshteinDistanceCalculator
from transcription_compare.tokenizer import CharacterTokenizer, WordTokenizer
from transcription_compare.utils import SimpleReferenceCombinationGenerator

from transcription_compare.results import AlignmentResult
alignment_result = AlignmentResult()
alignment_result.add_token(ref_token=None, output_tokens=["1"], add_to_left=False)
alignment_result.add_token(ref_token=None, output_tokens=["2"], add_to_left=False)
alignment_result.add_token(ref_token=None, output_tokens=["3"], add_to_left=False)
alignment_result.add_token(ref_token="1", output_tokens=["4"], add_to_left=False)
alignment_result.add_token(ref_token=None, output_tokens=["5"], add_to_left=False)
alignment_result.add_token(ref_token="ha", output_tokens=["in", "and", "some"], add_to_left=False)
alignment_result.add_token(ref_token="someday", output_tokens=["days"], add_to_left=False)
alignment_result.add_token(ref_token="one", output_tokens=["1"], add_to_left=False)
alignment_result.add_token(ref_token="two", output_tokens=["2"], add_to_left=False)
alignment_result.add_token(ref_token="and", output_tokens=["in", "and", "some"], add_to_left=False)
alignment_result.add_token(ref_token="someday", output_tokens=["days"], add_to_left=False)
alignment_result.add_token(ref_token="1", output_tokens=["1"], add_to_left=False)
alignment_result.add_token(ref_token="2", output_tokens=["2"], add_to_left=False)
alignment_result.add_token(ref_token="one", output_tokens=["one"], add_to_left=False)
alignment_result.add_token(ref_token="two", output_tokens=["two"], add_to_left=False)
alignment_result.add_token(ref_token="and", output_tokens=["in", "and", "some"], add_to_left=False)
alignment_result.add_token(ref_token="someday", output_tokens=["days"], add_to_left=False)
alignment_result.add_token(ref_token="one", output_tokens=["one"], add_to_left=False)
# alignment_result.add_token(ref_token="one", output_tokens=["one", "two", "three"], add_to_left=False)
# alignment_result.add_token(ref_token="and", output_tokens=["in", "and", "some"], add_to_left=False)
# alignment_result.add_token(ref_token="someday", output_tokens=["days"], add_to_left=False)
alignment_result.add_token(ref_token="one", output_tokens=["la", "two", "three"], add_to_left=False)
# alignment_result.add_token(ref_token="someday", output_tokens=["xi"], add_to_left=False)
alignment_result.add_token(ref_token="someday", output_tokens=["ays"], add_to_left=False)
alignment_result.merge_none_tokens()
print('alignment_result', alignment_result)
error_list = alignment_result.get_error_section_list()
for e in error_list:
    #  single
    #  to do get two line error section
    if len(e) == 2:
        #  need to have KUO check this len.. I made this. !!!!!!!!!!!!!!
        print('e2', e.original_alignment_result)
        print('e r', e.original_alignment_result.get_reference())
        #  need to have KUO check this len.. I made this. !!!!!!!!!!!!!!class AlignmentResult
        print('e o', e.original_alignment_result.get_outputs_list())
        all_reference = e.original_alignment_result.get_reference()
        all_output = e.original_alignment_result.get_outputs_list()
        print('all_reference', all_reference)
        print('all_output', all_output)
        print(len(all_output), all_output[0])
        #  get the index
        if all_reference[0] in all_output[0]:
            output_first_index = all_output[0].index(all_reference[0])
            output_first_flag = True
        else:
            output_first_flag = False
            output_first_index = 0
        if all_reference[1] in all_output[1]:
            output_second_flag = True
            output_second_index = all_output[1].index(all_reference[1])
        else:
            output_second_flag = False
            output_second_index = -1
        print('output_first_index', output_first_index)
        print('output_second_index', output_second_index)
        #  or this version
        # for i in range(len(all_reference)):
        #     name = 'output_{}_index'.format(i)
        #     name2 = 'output_{}_index_flag'.format(i)
        #     if all_reference[i] in all_output[i]:
        #         name = all_output[i].index(all_reference[i])
        #         name2 = True
        #     else:
        #         name = 0
        #         name2 = False

        # sort
        sort_output_list = list()
        # sort_output_list_first = list()
        # sort_output_list_second = list()

        tmp_first = list()
        tmp_second = list()
        #  both have flags
        if output_first_flag and output_second_flag:
            #  head
            tmp_first += all_output[0][:output_first_index+1]
            #  tail
            tmp_second += all_output[1][output_second_index:]
        # first have flag
        elif output_first_flag is True and output_second_flag is False:
            #  head
            tmp_first += all_output[0][:output_first_index+1]
            #  tail
            tmp_second.append(all_output[1][-1])
        # second have flag
        elif output_first_flag is False and output_second_flag is True:
            #  head
            tmp_first.append(all_output[0][0])
            #  tail
            tmp_second += all_output[1][output_second_index:]
        # both don't have flags
        else:
            #  head
            tmp_first.append(all_output[0][0])
            #  tail
            tmp_second.append(all_output[1][-1])
        print('tmp_first', tmp_first)
        print('tmp_second', tmp_second)
        # if output_first_index != len(all_output):
        #     for word in all_output[0][output_first_index:]:
        #         tmp_second.insert(0, word)
        # sort_output_list.append([tmp_first, tmp_second])
        assign_list = list()
        #  第一行需要分配的
        if len(all_output[0][output_first_index+1]) != 0:
            assign_list += all_output[0][output_first_index+1:]
        #  第二行需要分配的
        if len(all_output[1][:output_second_index]) != 0:
            assign_list += all_output[1][:output_second_index]
        print('assign_list', assign_list)
        # 如果有需要分配的
        if len(assign_list) != 0:
            for index in range(len(assign_list)+1):#  因为range 会减一
                # print('index, sort_output_list', index, sort_output_list)
                tmp_first_tmp = tmp_first.copy()
                tmp_second_tmp = tmp_second.copy()
                sort_output_list_tmp = list()
                # print('tmp_first_tmp', tmp_first_tmp)
                # print('tmp_second_tmp', tmp_second_tmp)
                tmp_first_tmp += assign_list[:index]
                # 第一个是0 就是空，全部在第二行的意思
                # #index= len(assign_list), 全部在第一行
                # tmp_second_tmp.insert(0, assign_list[index:])
                # print('assign_list[index:]', assign_list[index:])
                tmp_second_tmp = assign_list[index:]+tmp_second_tmp
                sort_output_list_tmp.append(tmp_first_tmp)
                sort_output_list_tmp.append(tmp_second_tmp)
                # print('index, sort_output_list_tmp', index, sort_output_list_tmp)
                # print('before, sort_output_list', index, sort_output_list)
                # print('before sort_output_list', sort_output_list)
                sort_output_list.append(sort_output_list_tmp)
                # print('after sort_output_list', sort_output_list)
                # print("!!!!!!!!!!")
            print('sort_output_list', sort_output_list)
            print('len_list', len(sort_output_list))
            ## to do calculate
            calculator = UKKLevenshteinDistanceCalculator(
                tokenizer=CharacterTokenizer(),
                get_alignment_result=False
            )
            old_distance = alignment_result.calculate_three_kinds_of_distance()[0]
            distance = calculator.get_distance(all_reference[0], sort_output_list[0]).distance
        #             for x in generator.get_all_reference():
        #                 x = " ".join(x)
        #                 distance = calculator.get_distance(x, output_string).distance

            d = 0
            for current_output in sort_output_list:
                print('current_reference', all_reference[0])
                print('current_output', current_output)
                d += calculator.get_distance(all_reference[0], current_output[0]).distance
                d += calculator.get_distance(all_reference[1], current_output[1]).distance
                print('old_distance', old_distance)
                print('d', d)
                if d < old_distance:
                    old_distance = distance
                    tmp_result = current_output
                print('tmp_result', tmp_result)
            if tmp_result is None:
                pass
            calculator2 = UKKLevenshteinDistanceCalculator(
                tokenizer=WordTokenizer(),
                get_alignment_result=True
            )
            update_result = calculator2.get_distance(all_reference[0], " ".join(tmp_result[0])).alignment_result
            update_result += calculator2.get_distance(all_reference[1], " ".join(tmp_result[1])).alignment_result
            print(update_result)


def update_alignment_result_word(alignment_result):
    # fist check same character
    for row in alignment_result:
        if row.reference in row.output:
            index = list.index(row.reference)
        else:
            index = 0
    # sort
    # return alignment_result
    pass

for e in error_list:
    if len(e) == 2:  # question we make it two lines or just check and use the two line??????????????
        updated_alignment_result = update_alignment_result_word(
            e.original_alignment_result)
    if updated_alignment_result is not None:
        # print(">>>>>>>>>>>>>not None")
        # print(updated_alignment_result)
        e.set_correction(updated_alignment_result)



#calculate cer
distance, substitution, insertion, deletion = alignment_result.calculate_three_kinds_of_distance()
#apply back
alignment_result.apply_error_section_list(error_list)




