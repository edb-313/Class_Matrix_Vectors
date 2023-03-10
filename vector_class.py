from math import acos


class Vector:
    def __init__(self, v=None, file_path=""):
        self.file_path = file_path
        if self.file_path == "":
            if v is None:
                v = []
            self.v = v
        else:
            self.v = self.create_vector_from_file(self.file_path)
        self.__length = len(self.v)
    
    def create_vector_from_file(self, file_path):
        file = open(file_path, 'r')
        line0 = file.readlines()[0]
        file.seek(0)
        lines = file.readlines()[2:]
        dim = int(line0.split('=')[-1])
        vec = [1.0 for x in range(0, dim)]
        for line in lines:
            s = line.replace('\n', '').split('\t')
            t = list(map(float, s))
            index = int(t[0])
            value = t[1]
            vec[index] = value
        return vec

    def get_vector_length(self):
        return self.__length

    def __add__(self, other):
        if isinstance(other, Vector):
            if self.__length == other.__length:
                x = Vector()
                for i in range(self.__length):
                    x.v.append(self.v[i] + other.v[i])
                return x
            else:
                print("The vectors are of different lengths")
        else:
            print("The second element is not of type vector")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            x = Vector()
            for i in range(self.__length):
                x.v.append(self.v[i] * other)
            return x
        else:
            print("The second element is not of type integer or float")

    def __str__(self):
        return str(self.v)

    def calculate_inner_product(self, other):
        if isinstance(other, Vector):
            if self.__length == other.__length:
                ip = 0
                for i in range(self.__length):
                    ip += self.v[i] * other.v[i]
                return ip
            else:
                print("The vectors are of different lengths")
        else:
            print("The second element is not of type vector")

    def calculate_magnitude(self):
        s = 0
        for i in range(self.__length):
            s += self.v[i] ** 2
        return s ** 0.5

    def calculate_angle_with_other_vector(self, other):
        if isinstance(other, Vector):
            return acos(self.calculate_inner_product(other) / (self.calculate_magnitude() * other.calculate_magnitude()))
        else:
            print("The second element is not of type vector")

    def calculate_cross_product(self, other):
        if isinstance(other, Vector):
            if self.__length == other.__length == 3:
                x = Vector()
                x.v.append(self.v[1] * other.v[2] - self.v[2] * other.v[1])
                x.v.append(self.v[2] * other.v[0] - self.v[0] * other.v[2])
                x.v.append(self.v[0] * other.v[1] - self.v[1] * other.v[0])
                return x
            else:
                print("The vectors are not of three dimensions")
        else:
            print("The second element not of type vector")


# v = Vector([1, 1, 1, 1, 1])
v = Vector(file_path=r'C:\Users\artes\PycharmProjects\ProgrammingFoundations\test_data\Vector_file_10_2.txt')
# print(v.v[1])
# print(v)
