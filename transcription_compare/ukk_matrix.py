from typing import List
import struct


class FKPColumn:
    """
    Represent one column in the FKP matrix.
    For each column, the first cell in P. All other cells have three properties:
        1. n: The number filled into the matrix
        2. source: could be one of [-1, 0, 1].
            If source == -1 at FKP[r, c], it means that the max value comes from FKP[r-1, c-1]
            If source == 0 at FKP[r, c], it means that the max value comes from FKP[r, c-1]
            If source == 1 at FKP[r, c], it means that the max value comes from FKP[r+1, c-1]
        3. n_match: count of match tokens
    """

    __slots__ = ("p", "n_list", "source_list", "n_match_list", "compressed_byte_array", "compressed_meta", "size")

    def __init__(self, p: int, size: int):
        """
        :param p: The first number in the column
        :param size: the size of the column
        """
        self.p = p
        self.n_list = [0] * size
        self.source_list = [None] * size
        self.n_match_list = [0] * size
        self.compressed_byte_array = None
        # store the meta data of compressed matrix: (n_skip, n_length, n_end(==n_skip + n_length))
        self.compressed_meta = None
        self.size = size

    def get_n(self, n_row: int):
        if n_row == 0:
            return self.p
        else:
            if self.is_compressed():
                n_real_row = n_row - 1
                if (n_real_row < self.compressed_meta[0]) or (n_real_row >= self.compressed_meta[2]):  # in skip section
                    return -10
                else:
                    s = 4 * (n_real_row - self.compressed_meta[0])
                    return struct.unpack(
                        "i", self.compressed_byte_array[0][s:(s + 4)])[0]
            else:
                return self.n_list[n_row]

    def set_n(self, n_row: int, new_n: int):
        if self.is_compressed():
            raise NotImplemented("Cannot set_n on compressed column")
        if n_row == 0:
            raise ValueError("Cannot set_n when n_row == 0. P value is set in the constructor")
        self.n_list[n_row] = new_n

    def get_source(self, n_row: int):
        if n_row == 0:
            return None
        else:
            if self.is_compressed():
                n_real_row = n_row - 1
                if (n_real_row < self.compressed_meta[0]) or (n_real_row >= self.compressed_meta[2]):  # in skip section
                    return None
                else:
                    s = n_real_row - self.compressed_meta[0]
                    tmp_source = struct.unpack("b", self.compressed_byte_array[1][s:(s + 1)])[0]
                    if tmp_source not in (-1, 0, 1):
                        return None
                    return tmp_source
            else:
                return self.source_list[n_row]

    def set_source(self, n_row: int, new_source):
        if self.is_compressed():
            raise NotImplemented("Cannot set_source on compressed column")
        if n_row == 0:
            raise ValueError("Cannot set_source when n_row == 0. The value at index 0 is P")
        if new_source not in (-1, 0, 1):
            raise ValueError("source value should be one of (-1, 0, 1)")
        self.source_list[n_row] = new_source

    def get_n_match(self, n_row: int):
        if n_row == 0:
            return 0
        else:
            if self.is_compressed():
                n_real_row = n_row - 1
                if (n_real_row < self.compressed_meta[0]) or (n_real_row >= self.compressed_meta[2]):  # in skip section
                    return 0
                else:
                    s = 4 * (n_real_row - self.compressed_meta[0])
                    return struct.unpack(
                        "i", self.compressed_byte_array[2][s:(s + 4)])[0]
            else:
                return self.n_match_list[n_row]

    def set_n_match(self, n_row: int, new_n_match):
        if self.is_compressed():
            raise NotImplemented("Cannot set_n_match on compressed column")
        if n_row == 0:
            raise ValueError("Cannot set_source when n_row == 0. The value at index 0 is P")
        self.n_match_list[n_row] = new_n_match

    def compress_to_byte_array(self):
        """
        Compress n_list, source_list and n_match_list to byte array (to efficiently use memory)
        :return:
        """
        n_skip = 0
        for i in self.n_list[1:]:
            if i < -1:
                n_skip += 1
            else:
                break
        n_start = n_skip + 1
        n_length = 0
        for i in self.n_list[n_start:]:
            if i >= -1:
                n_length += 1
            else:
                break
        self.compressed_meta = (n_skip, n_length, n_skip + n_length)
        new_source_list = []
        for i in self.source_list:
            if i is None:
                new_source_list.append(2)
            else:
                new_source_list.append(i)
        self.compressed_byte_array = (
            struct.pack('i' * n_length, * self.n_list[n_start:(n_start + n_length)]),
            struct.pack('b' * n_length, * new_source_list[n_start:(n_start + n_length)]),
            struct.pack('i' * n_length, * self.n_match_list[n_start:(n_start + n_length)])
        )
        self.n_list = None
        self.source_list = None
        self.n_match_list = None

    def is_compressed(self):
        """
        Check whether the column is compressed
        :return:
        """
        return not (self.compressed_byte_array is None)

    def print(self, print_all=False):
        out_str_list = [str(self.p)]
        for i in range(self.size - 1):
            if print_all:
                out_str_list.append(str((self.get_n(i + 1), self.get_source(i+1), self.get_n_match(i+1))))
            else:
                out_str_list.append(str(self.get_n(i + 1)))
        print("[" + ",".join(out_str_list) + "],")


class FKPMatrix:
    """
    The class to represent FKP matrix.
    To efficiently use memory, it compresses all cols instead of the last two
    """

    def __init__(self, first_col: List[int], keep_all_columns=False):
        """
        Initial the FKP matrix using first col (range(-(alen + 1), blen + 1))
        :param first_col:
        :param keep_all_columns:
            If set to True, the matrix will only keep the first column and the last two columns.
            It will save memory, but cannot do alignment
        """
        self.first_col_list = first_col
        self.keep_all_columns = keep_all_columns
        # load the first_col into FKPColumn object
        self.first_col = FKPColumn(p=-first_col[0], size=len(first_col))
        for (M, i) in enumerate(first_col[1:]):
            self.first_col.set_n(M+1, i)

        self.cols = [self.first_col]

    def append_col(self, new_col: FKPColumn):
        """
        Append a new column to the matrix.
        :param new_col:
        :return:
        """
        self.cols.append(new_col)

        if len(self.cols) > 3:
            if not self.keep_all_columns:
                # discard old columns when self.keep_all_columns == False
                while len(self.cols) > 3:
                    self.cols.pop(1)
            else:
                # compress old columns when self.keep_all_columns == True
                i = -3
                while i != (-len(self.cols)):
                    if not self.cols[i].is_compressed():
                        self.cols[i].compress_to_byte_array()
                    else:
                        break
                    i -= 1

    def get_first_col(self):
        """
        Return the first column of the FKP matrix. It's a list of integer
        :return:
        """
        return self.first_col_list

    def get_first_col_int(self, n_row: int):
        """
        Return the integer at n_row in the first column of FKP matrix
        :param n_row:
        :return:
        """
        return self.first_col_list[n_row]

    def get_col(self, n_col: int):
        """
        Return the column represented as FKPColumn object
        :param n_col
        :return:
        """
        if self.keep_all_columns:
            return self.cols[n_col]
        else:
            if n_col not in (0, -1, -2):
                raise ValueError("The FKPMatrix only keep first and last two columns. "
                                 + "Please use n_col=0 to get first column, "
                                 + "and n_col=-1/-2 to get last two columns")
            return self.cols[n_col]

    def get_n(self, n_row: int, n_col: int):
        return self.get_col(n_col).get_n(n_row)

    def get_source(self, n_row: int, n_col: int):
        return self.get_col(n_col).get_source(n_row)

    def get_n_match(self, n_row: int, n_col: int):
        return self.get_col(n_col).get_n_match(n_row)
    
    def get_all_in_cell(self, n_row: int, n_col: int):
        return self.get_n(n_row, n_col), self.get_source(n_row, n_col), self.get_n_match(n_row, n_col)

    def print(self, print_all=False):
        print("[")
        for i in self.cols:
            i.print(print_all)
        print("]")


def main():
    fkp_matrix = FKPMatrix(first_col=[-3, -2, -1, 0, 1, 2], keep_all_columns=True)
    fkp_matrix.print(print_all=True)

    for i in range(10):
        new_col = FKPColumn(p=i, size=7)
        for j in range(6):
            new_col.set_n(j+1, j)
            new_col.set_source(j+1, 1)
            new_col.set_n_match(j+1, j)
        new_col.set_n(1, -10)
        new_col.set_n(-1, -10)
        fkp_matrix.append_col(new_col)
        fkp_matrix.print(print_all=True)

    # for i in range(3000):
    #     new_col = FKPColumn(p=i, size=3001)
    #     for j in range(3000):
    #         new_col.set_n(j+1, j)
    #         new_col.set_source(j+1, 1)
    #         new_col.set_n_match(j+1, j)
    #     fkp_matrix.append_col(new_col)
    #     # fkp_matrix.print(print_all=True)
    # print(fkp_matrix.get_n(n_row=3, n_col=3))
    # print("done")
    # time.sleep(1000)


if __name__ == "__main__":
    main()
