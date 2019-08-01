# single or multi???????????????
#to do get two line error section
alignment_result = _get_alignment_result(
    fkp, row, col, s=ref_tokens_list, t=output_tokens_list
)

error_list = alignment_result.get_error_section_list()

def update_alignment_result(alignment_result):
    # fist check same character
    for row in alignment_result:
        if row.reference in row.output:
            index = list.index(row.reference)
        else:
            index = 0
    # sort

        return alignment_result

  for e in error_list:
    if len(e) == 2:  # question we make it two lines or just check and use the two line??????????????
        updated_alignment_result = update_alignment_result(
            e.original_alignment_result)
    if updated_alignment_result is not None:
        # print(">>>>>>>>>>>>>not None")
        # print(updated_alignment_result)
        e.set_correction(updated_alignment_result)



#calculate cer

distance, substitution, insertion, deletion = alignment_result.calculate_three_kinds_of_distance()
#apply back
alignment_result.apply_error_section_list(error_list)


