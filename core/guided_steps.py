import json
import os
import sys
__guide = {}
__steps = {}
def ejecute_steps(config=None):
    __guide = json.load(open("{0}/guide/guides.json".format(config["_path"]), "r"))
    __steps = json.load(open("{0}/guide/steps.json".format(config["_path"]), "r"))
    print("Guia Activa: {0}".format(__guide[__guide["guide_active"]]))
    _step_cont = 1
    for step in __guide[__guide["guide_active"]]:
        print("{2} - Ejecutando paso {0}: step : {1}".format(_step_cont,step,os.getpid()))
