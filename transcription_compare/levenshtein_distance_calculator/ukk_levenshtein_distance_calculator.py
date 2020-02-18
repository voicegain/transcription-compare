from .abstract_levenshtein_dsitance_calculator import AbstractLevenshteinDistanceCalculator
from transcription_compare.results import Result, AlignmentResult
from transcription_compare.ukk_matrix import FKPMatrix, FKPColumn
import time
from tqdm import tqdm
from transcription_compare.tokenizer import CharacterTokenizer
# from ..utils.error_display_method import update_alignment_result_word


class UKKLevenshteinDistanceCalculator(AbstractLevenshteinDistanceCalculator):

    def __init__(self, tokenizer, threshold=1, get_alignment_result=False, local_optimizers=None, is_master=False):
        super().__init__(tokenizer, get_alignment_result)
        self.threshold = threshold
        self.local_optimizers = local_optimizers
        self.is_master = is_master

    def get_result_from_list(self, ref_tokens_list, output_tokens_list):

        is_final, distance, fkp, row, col = self.ukk_threshold(
            a=ref_tokens_list,
            b=output_tokens_list
        )
        # print(distance)

        if self.get_alignment_result:
            # NOTE: SPLIT is not considered as an error. (ALWAYS when get_alignment_result == True)
            if not is_final:
                return Result(distance=distance, is_final=is_final, len_ref=len(ref_tokens_list),
                              len_output=len(output_tokens_list))
            else:
                alignment_result = self._get_alignment_result(
                    fkp, row, col, reference=ref_tokens_list, output=output_tokens_list
                )
                if self.local_optimizers is not None:
                    for local_optimizer in self.local_optimizers:
                        # print('local_optimizer', local_optimizer)

                        error_list = alignment_result.get_error_section_list()
                        for e in error_list:
                            # print("!!!!!!!!!!!!!!!!!!!!!!!")
                            # print('local_optimizer', local_optimizer)
                            # print('orginal' , e.original_alignment_result)
                            updated_alignment_result = local_optimizer.update_alignment_result_error_section(e)
                            if updated_alignment_result is not None:
                                # print(">>>>>>>>>>>>>not None")
                                # print(updated_alignment_result)
                                e.set_correction(updated_alignment_result)

                        alignment_result.apply_error_section_list(error_list)
                # print(">>>>>>>>>before calculate three")
                distance, substitution, insertion, deletion = alignment_result.calculate_three_kinds_of_distance()
                return Result(distance=distance,
                              substitution=substitution,
                              deletion=deletion,
                              insertion=insertion,
                              is_final=is_final,
                              len_ref=len(ref_tokens_list),
                              len_output=len(output_tokens_list),
                              alignment_result=alignment_result
                              )
        else:
            # NOTE: the distance comes from the UKK algorithm. (SPLIT is considered as an error)
            return Result(distance=distance, is_final=is_final, len_ref=len(ref_tokens_list),
                          len_output=len(output_tokens_list))

    def ukk_threshold(self, a, b):
        a_len = len(a)
        b_len = len(b)
        fkp, l_cols, l_rows, p = self._get_r_and_c_index(a, b)
        r = len(l_rows)

        count = 0
        last_col_is_created = False

        is_final = False
        distance = None
        row = 0

        if self.is_master:
            p_bar = tqdm(total=p)
        else:
            p_bar = None

        while not last_col_is_created:
            last_col_is_created, is_final, distance, row = self._create_next_col(
                fkp=fkp,
                first_value_in_new_col=l_cols[count],
                size=r, a=a, b=b, a_len=a_len, b_len=b_len, p=p
            )
            count += 1
            if self.is_master:
                p_bar.update()

        if p_bar is not None:
            p_bar.close()

        return is_final, distance, fkp, row, count

    def _get_r_and_c_index(self, a, b):
        a_len = len(a)
        b_len = len(b)
        p = int(self.threshold * max(a_len, b_len)) + 1

        l_rows = list(range(-(p + 1), p + 1))
        l_cols = list(range(-1, p))

        fkp = FKPMatrix(first_col=l_rows, keep_all_columns=self.get_alignment_result)
        return fkp, l_cols, l_rows, p

    @staticmethod
    def _create_next_col(fkp, first_value_in_new_col, size, a, b, a_len, b_len, p):
        """
        Return whether the last col is created (boolean)
        """
        first_col = fkp.get_first_col()  # FKP[:][0], list of integer
        last_col = fkp.get_col(-1)  # FKp[:][1], FKPColumn
        new_col = FKPColumn(p=first_value_in_new_col, size=size)  # FKP[:][2], FKPColumn

        mid = None
        distance = None
        rows = 0
        last_col_is_created = False
        for i in range(1, size):

            if last_col_is_created:
                break

            if new_col.get_n(0) == abs(first_col[i]) - 1:
                if first_col[i] < 0:
                    new_col.set_n(n_row=i, new_n=abs(first_col[i]) - 1)
                else:
                    new_col.set_n(n_row=i, new_n=-1)

            elif new_col.get_n(0) < abs(first_col[i]) - 1:
                new_col.set_n(n_row=i, new_n=-10)

            elif new_col.get_n(0) >= abs(first_col[i]):  # p=k or p>k-1

                t = last_col.get_n(n_row=i) + 1

                k_index = first_col[i]

                substitution = t
                insertion = last_col.get_n(n_row=i - 1)
                deletion = last_col.get_n(n_row=i + 1) + 1

                t = max(substitution, insertion, deletion)
                if t == substitution:
                    source_value = 0
                elif t == insertion:
                    source_value = -1
                else:
                    source_value = 1

                n_match = 0
                while (t < min(a_len, b_len - k_index)) and (a[t] == b[k_index + t]):
                    n_match += 1
                    t = t + 1
                new_col.set_n(n_row=i, new_n=t)
                new_col.set_source(n_row=i, new_source=source_value)
                new_col.set_n_match(n_row=i, new_n_match=n_match)

                cha = b_len - a_len
                if first_col[i] == cha and t == min(a_len, b_len - k_index):
                    new_col.set_n(n_row=i, new_n=t)
                    distance = new_col.get_n(0)
                    mid = True
                    rows = i
                    last_col_is_created = True

                elif first_col[i] == p - 1 and new_col.get_n(0) == p - 1:
                    mid = False
                    distance = new_col.get_n(0)
                    rows = i
                    last_col_is_created = True

                new_col.set_n(n_row=i, new_n=t)
        fkp.append_col(new_col=new_col)
        return last_col_is_created, mid, distance, rows

    def _get_alignment_result(self, fkp, row, col, reference, output):
        """
        we are trying to get all alignment result by the fkp, from the cell where row and col point us, to the
        end where the first cell. Don't get confused by the row and col.

        :param fkp: (f(k,p)array from the ukk, a two dimensional array having
        max_k rows whose indices correspond to d(i,j) array diagonal numbers and max_p columns whose indices range
        from -1 to the largest possible d(i,j) array cell value.)
        :param row: we should start getting alignment by this row. (the row is in the col)
        :param col: we should start getting alignment by this row. (the col is in the row)
        :param reference: reference string
        :param output: output string
        :return: alignment_result
        """

        alignment_result = AlignmentResult()
        count_for_output = 0
        reach_first_cell = False
        while not reach_first_cell:
            # we will only stop when it is first cell
            reach_first_cell, row, col, count_for_output = self._get_me_the_result_by_looping_through_each_col(
                fkp, row, col, count_for_output, reference, output, alignment_result
            )

        alignment_result.merge_none_tokens()
        return alignment_result

    def _get_me_the_result_by_looping_through_each_col(self, fkp, row, col, count_for_output, reference, output,
                                                       alignment_result):
        """
        we are tying to get specific alignment result here by looping through each col.
        eg:(1,2,3)
        1: we first look at if the third number is zo or not. it is zero, we just look at the second number;
        if it is not zero, which means the reference and the output are the same in this part,
         and the look at the second number.

        2: let' see what is the second number.

        :param fkp:
        :param row: we should start getting alignment by this row. (the row is in the col)
        :param col: we should start getting alignment by this row. (the col is in the row)
        :param count_for_output: get index of the output
        :param reference:
        :param output:
        :param alignment_result:
        :return: whether is first cell
        """
        # push same tokens to alignment_result (#3)
        # if it is not zero, which means the reference and the output are the same in this part.
        if fkp.get_n_match(n_row=row, n_col=col) > 0:  # 3
            for i in range(fkp.get_n_match(n_row=row, n_col=col)):
                count_for_output -= 1
                self._alignment_add(reference[fkp.get_n(n_row=row, n_col=col)-1-i], output[count_for_output],
                                    alignment_result)
        # distinguish insert / del / sub according to #2
        # no matter if the third number is zero or not, we will have to look at the second number;
        return self._second_number(row, col, count_for_output, reference, output, fkp, alignment_result)

    def _second_number(self, row, col, count_for_output, reference, output, fkp, alignment_result):
        """
        (the first number, the second number, the third number)
        there are several situation:
        1: if the second number is 1, it means we will have to delete one unit in the reference.
            next cell is the upper right.

        2: if the second number is -1, it means we will have to insert one unit in the output.
            next cell is the upper left.

        3: if the second number is 0, we need to do checking:
           3.1: if upper is not none.-> will do substitution. next cell is the upper.
           3.2: if upper is none.
                have to check if it is the first cell by checking if the second number in the upper three is none.
                -> if yes: we just keep.
                   because the reference and the output are the same in this (the first number) part.

                -> if the upper right is not none.
                   It means in the very beginning, we have to delete one unit. and keep doing step 3.
                -> if the upper left is not none.
                   It means in the very beginning, we have to insert one unit. and keep doing step 3.

        :param row: where we should look at
        :param col: where we should look at
        :param count_for_output: the part that we should look at output
        :param reference:
        :param output:
        :param fkp:
        :param alignment_result:
        :return: whether is first cell
        """
        #  1: if the second number is 1, it means we will have to delete one unit in the reference.
        #             next cell is the upper right by _next_move.
        if fkp.get_source(n_row=row, n_col=col) > 0:  # 2 means delete
            self._alignment_add(
                reference[fkp.get_n(n_row=row, n_col=col) - 1 - fkp.get_n_match(n_row=row, n_col=col)],
                None,
                alignment_result
            )

        # 2: if the second number is -1, it means we will have to insert one unit in the output.
        #             next cell is the upper left by _next_move.
        elif fkp.get_source(n_row=row, n_col=col) < 0:  # 2 insert: #means insert

            count_for_output -= 1
            self._alignment_add(None, output[count_for_output], alignment_result)
            # print('insert', alignment_result)

        # if it is 0.
        # if the upper one is not None, do sub.
        # if not, we will check upper in the while.
        elif fkp.get_source(n_row=row, n_col=col) == 0:  # 2 sub
            if fkp.get_source(n_row=row, n_col=col - 1) is not None:
                count_for_output -= 1
                # sub
                self._alignment_add(
                    reference[fkp.get_n(n_row=row, n_col=col) - 1 - fkp.get_n_match(n_row=row, n_col=col)],
                    output[count_for_output],
                    alignment_result)

        while True:
            #
            reach_first_cell, row, col, count_for_output, current_move_done = self._next_move(
                row, col, count_for_output, reference, output, fkp, alignment_result
            )
            if current_move_done:
                break
        return reach_first_cell, row, col, count_for_output

    def _next_move(self, row, col, count_for_output, reference, output, fkp, alignment_result):
        """
        wo do next move because we need to know where to end the process.

        1: check if it is the first cell by calling _next_one_step_move.
         it will return is_first_cell, next_movement_direction, upper_cell_is_none_but_has_not_none_neighbor.
         If the is_first_cell is True, we will end all the process. return none.

        2: it not the first cell. it will return direction of next cell back to _second_number

        3: because in the _second_number, we don't process two situations, because the rules are different:
           one is insert in the very beginning; two is delete in the very beginning. So we do it here.
           and it will return direction of next cell back to _second_number.
        :param row:
        :param col:
        :param count_for_output:
        :param reference:
        :param output:
        :param fkp:
        :param alignment_result:
        :return: reach_first_cell, row, col, count_for_output, current_move_done
        """
        is_first_cell, next_movement_direction, upper_cell_is_none_but_has_not_none_neighbor = self._next_one_step_move(
            row, col, fkp)
        # 1: check if it is the first cell by calling _next_one_step_move.
        #          it will return is_first_cell, next_movement_direction, upper_cell_is_none_but_has_not_none_neighbor.
        #          If the is_first_cell is True, we will end all the process. return none.
        if is_first_cell:
            # directly return. We only care the first return value
            return is_first_cell, None, None, None, True

        next_row = row + next_movement_direction
        next_col = col - 1
        # 2: it not the first cell. it will return direction of next cell back to _second_number
        if not upper_cell_is_none_but_has_not_none_neighbor:
            # here upper cell is not None, has number
            # is_first_cell == False
            return is_first_cell, next_row, next_col, count_for_output, True

        # 3: because in the _second_number, we don't process two situations, because the rules are different:
        #            one is insert in the very beginning; two is delete in the very beginning. So we do it here.
        if next_movement_direction == -1:
            # move left, insert
            count_for_output -= 1
            self._alignment_add(None, output[count_for_output], alignment_result)
            # print('insert',alignment_result)
            return is_first_cell, next_row, next_col, count_for_output, False

        else:
            self._alignment_add(
                reference[fkp.get_n(n_row=next_row, n_col=next_col) - fkp.get_n_match(n_row=next_row, n_col=next_col)],
                None,
                alignment_result
            )

            return is_first_cell, next_row, next_col, count_for_output, False

    @staticmethod
    def _next_one_step_move(row, col, fkp):
        """
        get_source means get the number in the middle.

        we are checking if current cell is the first cell or not.
        If the second number in the current cell is 1, it means this is not the first cell, and we should go upper right
        If the second number in the current cell -1, it means this is not the first cell, and we should go upper left.

        If the second number in the current cell 0, we should check what is the upper one.
        -> if upper three are all none: we just keep the ref and output.
           because the reference and the output are the same in this (the first number) part.

        -> if the upper right is not none.
           It means in the very beginning, we have to delete one unit. and keep doing step 3.
        -> if the upper left is not none.
           It means in the very beginning, we have to insert one unit. and keep doing step 3.




        :param row:
        :param col:
        :param fkp:
        :return:
            is_first_cell: boolean. whether the cell is first cell
            next_movement_direction: -1, 0, 1
                -1 means go up and left
                0 means go up
                1 means go up and right
            upper_cell_is_none_but_has_not_none_neighbor: boolean.
                Whether current movement is not sufficient to do the next token alignment
        """
        if fkp.get_source(n_row=row, n_col=col) == 1:
            # It cannot be the first_cell. We move up and right
            return False, 1, False

        elif fkp.get_source(n_row=row, n_col=col) == -1:
            # It cannot be the first_cell. We move up and left
            return False, -1, False

        else:
            # We need to check the cell above the decide
            col_move_up_by_one = col - 1
            if fkp.get_source(n_row=row, n_col=col_move_up_by_one) is not None:  # above
                # It cannot be the first cell. We move up
                return False, 0, False

            else:
                # We need to check left and right neighbors of the cell above to see whether it's the first cell

                left_neighbor_source = fkp.get_source(n_row=row - 1, n_col=col_move_up_by_one)
                right_neighbor_source = fkp.get_source(n_row=row + 1, n_col=col - 1)

                if (left_neighbor_source is None) and (right_neighbor_source is None):
                    # It's the first cell when both neighbors are None
                    return True, None, False

                elif left_neighbor_source is not None:
                    return False, -1, True

                else:
                    return False, 1, True

    @staticmethod
    def _alignment_add(s_index, t_index, alignment_result):
        """
        Just a wrapper of alignment_result.add_token() method
        :param s_index:
        :param t_index:
        :param alignment_result:
        :return:
        """
        if t_index is None:
            output = []
        else:
            output = [t_index]
        alignment_result.add_token(
            ref_token=s_index,
            output_tokens=output,
            add_to_left=True)
