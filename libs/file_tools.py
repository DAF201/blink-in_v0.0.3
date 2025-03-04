from hashlib import sha256
from pickle import dumps, loads
from io import BytesIO
from math import sqrt, ceil


# slice into x bytes, as github has max size of 25mb each
def data_slice(data, chunk_size):
    if type(data) != bytes:
        data = dumps(data)
    return [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]


# hash each chunk
def data_hash(chunks):
    return {x: sha256(chunks[x]).hexdigest() for x in range(len(chunks))}


# test purpose, not used yet
def virtual_file(data):
    if type(data) != bytes:
        data = dumps(data)
    return BytesIO(data)


# for encoding
def data_dimension_rounding(data_size):
    size = ceil(sqrt(data_size))
    if size**2 - data_size < 4:
        size += 1
    return size


def test_storage(file_name, file_body):
    with open(".\\temp\\%s" % file_name, "wb") as file:
        file.write(file_body)
