from .abstract_levenshtein_dsitance_calculator import AbstractLevenshteinDistanceCalculator
from ..results import Result, AlignmentResult
from ..ukk_matrix import FKPMatrix, FKPColumn
import time
from ..tokenizer import CharacterTokenizer
# from ..utils.error_display_method import update_alignment_result_word


class UKKLevenshteinDistanceCalculator(AbstractLevenshteinDistanceCalculator):

    def __init__(self, tokenizer, threshold=1, get_alignment_result=False, local_optimizers=None):
        super().__init__(tokenizer, get_alignment_result)
        self.threshold = threshold
        self.local_optimizers = local_optimizers

    def get_result_from_list(self, ref_tokens_list, output_tokens_list):
        start = time.clock()

        is_final, distance, fkp, row, col = self.ukk_threshold(
            a=ref_tokens_list,
            b=output_tokens_list
        )

        if self.get_alignment_result:
            if not is_final:
                return Result(distance=distance, is_final=is_final, len_ref=len(ref_tokens_list))
            else:
                alignment_result = self._get_alignment_result(
                    fkp, row, col, s=ref_tokens_list, t=output_tokens_list
                )
                if self.local_optimizers is not None:
                    for local_optimizer in self.local_optimizers:

                        error_list = alignment_result.get_error_section_list()
                        for e in error_list:
                            # print("!!!!!!!!!!!!!!!!!!!!!!!")
                            # print('local_optimizer', local_optimizer)
                            # print(e.original_alignment_result)
                            updated_alignment_result = local_optimizer.update_alignment_result_error_section(e)
                            if updated_alignment_result is not None:
                                # print(">>>>>>>>>>>>>not None")
                                # print(updated_alignment_result)
                                e.set_correction(updated_alignment_result)
                            # print(" None")
                        alignment_result.apply_error_section_list(error_list)
                # print(">>>>>>>>>before calculate three")
                distance, substitution, insertion, deletion = alignment_result.calculate_three_kinds_of_distance()
                return Result(distance=distance,
                              substitution=substitution,
                              deletion=deletion,
                              insertion=insertion,
                              is_final=is_final,
                              len_ref=len(ref_tokens_list),
                              alignment_result=alignment_result
                              )
        else:
            return Result(distance=distance, is_final=is_final, len_ref=len(ref_tokens_list))

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

        while not last_col_is_created:
            last_col_is_created, is_final, distance, row = self._create_next_col(
                fkp=fkp,
                first_value_in_new_col=l_cols[count],
                size=r, a=a, b=b, a_len=a_len, b_len=b_len, p=p
            )
            count += 1
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

    def _get_alignment_result(self, fkp, row, col, s, t):
        alignment_result = AlignmentResult()
        count = 0
        reach_first_cell = False
        while not reach_first_cell:
            reach_first_cell, row, col, count = self._get_me_the_result(
                fkp, row, col, count, s, t, alignment_result
            )

        alignment_result.merge_none_tokens()
        return alignment_result

    def _get_me_the_result(self, fkp, row, col, count, s, t, alignment_result):
        """
        Good name
        :param fkp:
        :param row:
        :param col:
        :param count:
        :param s:
        :param t:
        :param alignment_result:
        :return: whether is first cell
        """
        # push same tokens to alignment_result (#3)
        if fkp.get_n_match(n_row=row, n_col=col) > 0:  # 3
            for i in range(fkp.get_n_match(n_row=row, n_col=col)):
                count -= 1
                self._alignment_add(s[fkp.get_n(n_row=row, n_col=col)-1-i], t[count], alignment_result)
        # distinguish insert / del / sub according to #2
        return self._second_number(row, col, count, s, t, fkp, alignment_result)

    def _second_number(self, row, col, count, s, t, fkp, alignment_result):
        """
        :param row:
        :param col:
        :param count:
        :param s:
        :param t:
        :param fkp:
        :param alignment_result:
        :return: whether is first cell
        """
        if fkp.get_source(n_row=row, n_col=col) > 0:  # 2 means delete
            self._alignment_add(
                s[fkp.get_n(n_row=row, n_col=col) - 1 - fkp.get_n_match(n_row=row, n_col=col)],
                None,
                alignment_result
            )

        elif fkp.get_source(n_row=row, n_col=col) == 0:  # 2 sub
            if fkp.get_source(n_row=row, n_col=col - 1) is not None:
                count -= 1
                # sub
                self._alignment_add(
                    s[fkp.get_n(n_row=row, n_col=col) - 1 - fkp.get_n_match(n_row=row, n_col=col)],
                    t[count],
                    alignment_result)

        elif fkp.get_source(n_row=row, n_col=col) < 0:  # 2 insert: #means insert

            count -= 1
            self._alignment_add(None, t[count], alignment_result)
            # print('insert', alignment_result)
        return self._nextmove(row, col, count, s, t, fkp, alignment_result)

    def _nextmove(self, row, col, count, s, t, fkp, alignment_result):
        """

        :param row:
        :param col:
        :param count:
        :param s:
        :param t:
        :param fkp:
        :param alignment_result:
        :return: whether is first cell
        """
        is_first_cell, is_left, row, col = self._firstcell(row, col, fkp)

        if is_first_cell is False:  # not the first cell
            if is_left is None:
                return False, row, col, count
                # self._get_me_the_result(fkp, row, col, count, s, t, alignment_result)
            elif is_left:  # insert
                count -= 1
                self._alignment_add(None, t[count], alignment_result)
                # print('insert',alignment_result)
                return self._nextmove(row, col, count, s, t, fkp, alignment_result)
            elif not is_left:
                # delete
                self._alignment_add(
                    s[fkp.get_n(n_row=row, n_col=col) - fkp.get_n_match(n_row=row, n_col=col)],
                    None,
                    alignment_result
                )
                # alignment_add(S[FKP.get_n(n_row=row ,n_col=col)-1-FKP.get_n_match(n_row=row ,n_col=col)], None)
                # print(alignment_result)
                return self._nextmove(row, col, count, s, t, fkp, alignment_result)
        else:
            return True, None, None, None

    @staticmethod
    def _firstcell(row, col, fkp):
        """

        :param row:
        :param col:
        :param fkp:
        :return:  is_first_cell, is_left, row, col
        """
        # print(fkp.get_all_in_cell(n_row=row, n_col=col))
        if fkp.get_source(n_row=row, n_col=col) == 1:

            return False, None, row + 1, col - 1
        elif fkp.get_source(n_row=row, n_col=col) == -1:
  
            return False, None, row - 1, col - 1
        elif fkp.get_source(n_row=row, n_col=col - 1) is not None:  # above
     
            return False, None, row, col - 1
        elif fkp.get_source(n_row=row, n_col=col - 1) is None:
            if fkp.get_source(n_row=row - 1, n_col=col - 1) is None:  # left
                if fkp.get_source(n_row=row + 1, n_col=col - 1) is None:  # right
   
                    return True, None, row, col  # this is first cell
                else:
           
                    return False, False, row + 1, col - 1  # right
            else:
             
                return False, True, row - 1, col - 1

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
