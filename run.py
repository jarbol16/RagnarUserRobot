import sys
import json
import os
import asyncio
from core import ragnar as ra
import multiprocessing
from multiprocessing import Process
import time
import random
from core import functions_common as fc
import argparse

def eye(data,guide,steps):
    if "threads_active" in data and data["threads_active"]:
        if data["threads"]["guide_dynamic"]:
            data.update({"guide_dynamic_active": multiprocessing.current_process().name.split("#")[1]})
    try:
        if "periodic_iteration" in data and data["periodic_iteration"]["active"]:
            if data["periodic_iteration"]["minutes_sleep"] > 0:
                dr = None
                while True:
                    dr = ra.__init(config=data, dr=dr, guide=guide, steps=steps)
                    time.sleep(int(data["periodic_iteration"]["minutes_sleep"]))
        else:
            ra.__init(config=data, guide=guide, steps=steps)
    except Exception as ex:
        print("Error in main {0}".format(ex))


def guides_actives(data):
    GUIDES_ACTIVES = []
    if data["threads"]["guide_dynamic"]:
        data_guides = fc.read_file("guide/guides.json")
        for guide_name in data_guides[data["threads"]["guide_group_key"]]:
            GUIDES_ACTIVES.append({
                "name_guide": guide_name,
                "free": True
            })
    return GUIDES_ACTIVES


def get_next_guide_free(GUIDES_ACTIVES=[]):
    _guide = None
    for guide in GUIDES_ACTIVES:
        if guide["free"]:
            _guide = guide
            guide["free"] = False
            return [GUIDES_ACTIVES, _guide]
    if _guide is None:
        for guide in GUIDES_ACTIVES:
            guide["free"] = True
        _guide = GUIDES_ACTIVES[0]
    return [GUIDES_ACTIVES, _guide]


if __name__ == "__main__":
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()

    __path = os.getcwd()
    configurations = fc.read_file("config/setting.json")
    configurations.update({"_path": __path})
    __guide = json.load(open("{0}/guide/guides.json".format(configurations["_path"]), "r"))
    __steps = json.load(open("{0}/guide/{1}.json".format(configurations["_path"], __guide["file_steps"]), "r"))

    [configurations,__guide,__steps] = fc.read_args(config=configurations, guide=__guide,steps=__steps)

    try:
        if "threads_active" in configurations and configurations["threads_active"]:
            GUIDES_ACTIVES = guides_actives(configurations)
            PoolTheads = []
            for i in range(0, configurations["threads_num"]):
                print("Crendo sesion {0}".format(i))
                guide_name = ""
                if configurations["threads"]["guide_dynamic"]:
                    [GUIDES_ACTIVES, guide_active] = get_next_guide_free(GUIDES_ACTIVES)
                    guide_name = guide_active["name_guide"]
                p = Process(target=eye, args=(configurations, __guide, __steps,))
                p.name = "Sesion{0}#{1}".format(i, guide_name)
                PoolTheads.append(p)
            for pro in PoolTheads:
                print("Arrancando proceso {0}".format(pro.name))
                if configurations["threads"]["range_time_init"] > 0:
                    time_random = random.randint(1, int(configurations["threads"]["range_time_init"]))
                    print("Esperando {0}s para Arrnacar".format(time_random))
                    time.sleep(time_random)
                pro.start()
        else:
            eye(configurations, __guide, __steps)
    except Exception as ex:
        print("Error in main {0}".format(ex))
