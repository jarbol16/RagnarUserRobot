import os
import json
import argparse


def remove_file(file_anme=None, _path=None):
    try:
        print("Borrando imagen {0}/out/{1}.png".format(_path, file_anme))
        os.remove("{0}/out/{1}.png".format(_path, file_anme))
    except:
        pass


def read_file(_path=None):
    file = open("{0}/{1}".format(os.getcwd(), _path), "r")
    data = json.load(file)
    return data


def read_args(config, guide, steps):
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return [config, guide, steps]