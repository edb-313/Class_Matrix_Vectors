import random
import copy
from vector_class import Vector

random.seed(10)


class Matrix:
    def __init__(self, matrix=None, file_path=""):
        self.file_path = file_path
        if self.file_path == "":
            if matrix is None:
                matrix = [[]]
            if type(matrix[0]) == list:
                x = len(matrix[0])
                for e in matrix:
                    if len(e) == x:
                        x = len(e)
                    else:
                        print("Matrix rows aren't all of the same length")
                        raise SystemExit()
                self.matrix = matrix
            else:
                print("Please input a valid matrix")
                raise SystemExit()
        else:
            self.matrix = self.create_matrix_from_file(self.file_path)
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])

    def create_matrix_from_file(self, file_path):
        f = open(file_path, 'r')
        line0 = f.readlines()[0]
        f.seek(0)
        lines = f.readlines()[2:]
        dim = int(line0.split('=')[-1])
        m = []
        for i in range(0, dim):
            m.append([])
            for j in range(0, dim):
                m[i].append(0)
        for line in lines:
            s = line.split('\t')
            t = list(map(float, s))
            t1 = int(t[0])
            t2 = int(t[1])
            value = t[2]
            m[t1][t2] = value
        return m

    def create_empty_matrix(self, rows=None, cols=None):
        if rows is None and cols is None:
            rows = self.rows
            cols = self.cols
        return Matrix([[0 for j in range(cols)] for i in range(rows)])

    def __str__(self):
        printed_matrix = '\n'
        printed_matrix += '------------- output -------------\n'
        for row in range(self.rows):
            printed_matrix += ('|' + ', '.join(map(lambda x: '{0:10.5f}'.format(x), self.matrix[row])) + '| \n')
        printed_matrix += '----------------------------------'
        return printed_matrix

    def check_dimension(self, other):
        if self.rows == other.rows:
            if self.cols == other.cols:
                return True
        print("Matrices aren't of the same dimension")
        raise SystemExit()

    def __add__(self, other_matrix):
        if self.check_dimension(other_matrix):
            addition_matrix = self.create_empty_matrix()
            for row in range(self.rows):
                for col in range(self.cols):
                    addition_matrix.matrix[row][col] = (self.matrix[row][col] + other_matrix.matrix[row][col])
            return addition_matrix

    def __sub__(self, other_matrix):
        if self.check_dimension(other_matrix):
            subtraction_matrix = self.create_empty_matrix()
            for row in range(self.rows):
                for col in range(self.cols):
                    subtraction_matrix.matrix[row][col] = (self.matrix[row][col] - other_matrix.matrix[row][col])
            return subtraction_matrix

    def __mul__(self, other):
        if isinstance(other, (int, float, Matrix)):
            if type(other) == Matrix:
                if self.cols == other.rows:
                    multiplication_matrix = self.create_empty_matrix(self.rows, other.cols)
                    for row in range(self.rows):
                        for col in range(other.cols):
                            c = 0
                            for k in range(self.cols):
                                c += self.matrix[row][k] * other.matrix[k][col]
                            multiplication_matrix.matrix[row][col] = c
                    return multiplication_matrix
                else:
                    print(
                        "The number of rows of the second Matrix is not equivalent to the number of colums of the first")
            else:
                multiplication_matrix = self.create_empty_matrix()
                for row in range(self.rows):
                    for col in range(self.cols):
                        multiplication_matrix.matrix[row][col] = (self.matrix[row][col] * other)
                return multiplication_matrix
        else:
            print("Second element is not an integer, float or Matrix")

    def transpose(self):
        transposed_matrix = self.create_empty_matrix(self.cols, self.rows)
        for row in range(self.rows):
            for col in range(self.cols):
                transposed_matrix.matrix[col][row] = self.matrix[row][col]
        return transposed_matrix

    def remove_row_and_column(self, r, c):
        copyMatrix = copy.deepcopy(self)
        del copyMatrix.matrix[r]
        for row in range(len(copyMatrix.matrix)):
            del copyMatrix.matrix[row][c]
        return copyMatrix

    def reduce_lower_rows(self, m, rp, cp, v, ops):
        give_back_matrix = m.copy()
        give_back_vector = v.copy()
        for r in range(rp, len(m) - 1):
            val = give_back_matrix[r + 1][cp]
            ratio = give_back_matrix[r + 1][cp] / give_back_matrix[rp][cp]
            give_back_vector[r + 1] = give_back_vector[r + 1] - (give_back_vector[rp] * ratio)
            if val != 0:
                for c in range(cp, len(m)):
                    # if this number needs to be set to 0:
                    give_back_matrix[r + 1][c] = give_back_matrix[r + 1][c] - (give_back_matrix[rp][c] * ratio)
                    ops += 1
            # if value = 0 we dont need to to anything
            else:
                pass
        return give_back_matrix, give_back_vector, ops

    def row_reduce(self, other=None):  # , other=None
        ops = 0
        reduced_matrix = self.matrix.copy()
        reduced_vector = other.v
        # reduced_vector = [1 for x in range(self.rows)]
        row_pivot, column_pivot = 0, 0
        nr_of_swaps = 0
        try:
            for pivot in range(len(self.matrix[row_pivot]) - 1):  # two 'steps' in the case of 3x3 matrix
                pivot_value = self.matrix[row_pivot][column_pivot]

                # if pivot value is 1 or another non zero number we can reduce the lower rows:
                if pivot_value != 0:
                    function_output = self.reduce_lower_rows(reduced_matrix, row_pivot, column_pivot, reduced_vector, ops)
                    reduced_matrix, reduced_vector, ops = function_output

                # if pivot value is 0 we need another row to swap. After we reduce the lower rows
                if pivot_value == 0:
                    swapped_matrix = reduced_matrix.copy()
                    while pivot_value == 0:
                        n = 1
                        nr_of_swaps += 1
                        temp = reduced_matrix.copy()
                        swapped_matrix[row_pivot] = temp[row_pivot + n]
                        swapped_matrix[row_pivot + n] = temp[row_pivot]
                        pivot_value = swapped_matrix[row_pivot][column_pivot]
                        n += 1
                    function_output = self.reduce_lower_rows(swapped_matrix, row_pivot, column_pivot, reduced_vector)
                    reduced_matrix, reduced_vector, ops = function_output
                row_pivot += 1
                column_pivot += 1
            return Matrix(reduced_matrix), Vector(reduced_vector), ops
        except:
            print("Your input is not valid for a row-reduction. Please check your input")

    def determinant(self):
        reduced_matrix = self.row_reduce()[0]
        determinant = 1
        for row in range(self.rows):
            determinant *= reduced_matrix.matrix[row][row]
        return determinant
