import os

def read_file(filename):
    base_path = "/app/data/"
    full_path = base_path + filename

    with open(full_path, "r") as f:
        return f.read()

user_file = input("File name: ")
print(read_file(user_file))