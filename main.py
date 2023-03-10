from imports import *

# Change the filepath to your specific path where you stored the files
input_matrix = Matrix(file_path=r'C:\Users\artes\PycharmProjects\ProgrammingFoundations\test_data\Matrix_file_10.txt')
# In case we assume a vector of 1s
input_vector = Vector([1 for x in range(input_matrix.rows)])

st = time.time()

# Step 1: get the reduced matrix and the reduced vector
# input 'input_vector' if you have vector as a file, otherwise 1s vector is created
reduced = input_matrix.row_reduce(input_vector)  # input_vector
reduced_matrix, reduced_vector, ops = reduced

# step 2: execute the gaussian algorithm
solutions, ops = gaussian_distribution(reduced_matrix, reduced_vector, ops)


et = time.time()
elapsed_time = [et - st, 1000*(et - st)]

# extra step: round the values of the solutions
solutions_rounded = [round(x, 3) for x in solutions]

print(f"\n___The solutions for x___ \n{solutions_rounded}")
print(f"\n___Time passed___ \n{elapsed_time[1]: .6f} milliseconds or {elapsed_time[0]: .6f} seconds")

# Step 3: check the solutions!
print(f"\n___List of differences rounded to 4 digits (should be 0s)___ \n{check_solution(reduced_matrix, solutions, reduced_vector)}")

print(f"\n___Operations in total___ {ops}")
