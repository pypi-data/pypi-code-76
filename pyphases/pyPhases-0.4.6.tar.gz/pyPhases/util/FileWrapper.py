import tempfile
import os

# class FileWrapper:
def wrapWrite(writeFunction):
    path = os.path.join(tempfile.mkdtemp(), next(tempfile._get_candidate_names()))
    writeFunction(path)
    file = open(path, "rb")
    data = file.read()
    file.close()
    os.remove(path)
    return data

# class FileWrapper:
def wrapRead(readFunction, data):
    path = os.path.join(tempfile.mkdtemp(), next(tempfile._get_candidate_names()))
    file = open(path, "wb")
    file.write(data)
    file.close()

    ret = readFunction(path)
    os.remove(path)
    return ret
