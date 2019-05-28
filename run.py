import sys
import json
import os
from core import ragnar as ra
import asyncio
from multiprocessing import Process

def eye(data):
    try:
        ra.__init(config=data)
    except Exception as ex:
        print("Error in main {0}".format(ex))

if __name__=="__main__":
    __path = os.getcwd()
    try:
        file = open("{0}/config/setting.json".format(__path), "r")
        data = json.load(file)
        data.update({"_path": __path})
        if "threads_active" in data and data["threads_active"]:
            PoolTheads = []
            for i in range(0,data["threads_num"]):
                print("Crendo sesion {0}".format(i))
                p = Process(target=eye, args=(data,))
                p.name = "Sesion_{0}".format(i)
                PoolTheads.append(p)
            for pro in PoolTheads:
                print("Arrancando proceso {0}".format(pro.name))
                pro.start()
        else:
            eye(data)
    except Exception as ex:
        print("Error in main {0}".format(ex))
