def gaussian_distribution(matrix, vector, ops=0):
    n = matrix.cols
    vars_list = [x for x in range(n)]
    vars_list[-1] = vector.v[-1] / matrix.matrix[vars_list[-1]][vars_list[-1]]
    for k in reversed(vars_list[:-1]):
        v1 = (1/matrix.matrix[k][k])
        v2 = vector.v[k]
        v3 = 0
        for j in range(k + 1, n):
            v3 += matrix.matrix[k][j] * vars_list[j]
        value = v1 * (v2 - v3)
        vars_list[k] = value
    return vars_list, ops


def check_solution(matrix, solutions, vector):
    """
    Ax = b is the system we will solve. b - Ax should be approximately 0
    :return: set of differences
    """
    results = []
    for index in range(len(vector.v)):
        result1 = vector.v[index]
        result2 = 0
        for index2 in range(len(matrix.matrix[index])):
            result2 += matrix.matrix[index][index2] * solutions[index2]
        result = round(result1 - result2, 4)
        results.append(result)
    return results
