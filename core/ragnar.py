from selenium import webdriver
from selenium.common import  exceptions
from . import functions_common as fc
from connection.email import Email
import os


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import json
import time
global __session
global __driver
global __setting
global __email
#__driver = webdriver.Chrome()


def __init(config = None):
    """
    Inicio de robot ragnar
    :param config:
    :return:
    """
    global __email
    global __driver
    global __setting
    __email = Email()
    print("Ragnar comenzando a trabajar \n{0}".format(config))
    __setting = config
    if config["driver"]["chrome"]:
        __driver = webdriver.Chrome(executable_path="{0}/{1}".format(config["_path"],config["driver_url"]["chrome"]))
    elif config["driver"]["edge"]:
        __driver = webdriver.Edge(executable_path="{0}/{1}".format(config["_path"], config["driver_url"]["edge"]))
    elif config["driver"]["firefox"]:
        __driver = webdriver.Firefox(executable_path="{0}/{1}".format(config["_path"], config["driver_url"]["firefox"]))
    else:
        pass

    ejecute_steps(config=config)
    print("{0} - TERMINO".format(os.getpid()))

__guide = {}
__steps = {}


def ejecute_steps(config=None):
    global __driver
    #__driver = webdriver.Chrome()
    __guide = json.load(open("{0}/guide/guides.json".format(config["_path"]), "r"))
    __steps = json.load(open("{0}/guide/steps.json".format(config["_path"]), "r"))
    print("Guia Activa: {0}".format(__guide[__guide["guide_active"]]))
    _step_cont = 1
    for step in __guide[__guide["guide_active"]]:
        try:
            print("{2} - Ejecutando paso {0}: step : {1}".format(_step_cont, step, os.getpid()))
            _step_cont +=1
            _step_key = [k for k in step.keys()][0]
            _step = __steps[_step_key]
            if _step is not None:
                if "url" in _step:
                    __driver.get("{0}{1}".format(config["web_url_init"],_step["url"]))
                needs = [n for n in _step.keys() if "need" in n]
                for _need in needs:
                    elem = __driver.find_element_by_id(_step[_need])
                    elem.send_keys(step[_step_key][_need])
                acctions = [n for n in _step.keys() if "acction" in n]
                if acctions:
                    for ac in acctions:
                        print("{3} - Procesando accion {0}_{1}_{2}".format(__guide["guide_active"],_step_key,_step[ac]["id"],os.getpid()))
                        screenshot("{0}_{1}_{2}".format(__guide["guide_active"],_step_key,_step[ac]["id"]))
                        elem = __driver.find_element_by_id(_step[ac]["id"])
                        if elem:
                            img_anem = "{0}_{1}_{2}".format(__guide["guide_active"], _step_key, _step[ac]["id"])
                            event_in_elem(elem,_step[ac]["event"],sec=_step[ac]["time"],img=img_anem,action=_step[ac])
        except Exception as ex:
            print("No se sigue con la Guia")



def event_in_elem(elm,evt, sec=1,img="",action={}):
    global __setting
    global __email
    global __driver
    if "click" in evt:
        elm.click()
    time.sleep(3)
    screenshot("ANS_{0}".format(img))
    if search_error() is False:
        if "activate_wait" in action and action["activate_wait"]:
            encontro = wait(sec=sec,id=action["id_flag"])
            print("Encontro", encontro)
        else:
            time.sleep(sec)
            print("Debe borrar {0}_{1}".format(img,os.getpid()))
            fc.remove_file(file_anme="{0}_{1}".format(img,os.getpid()),_path= __setting["_path"])
            fc.remove_file(file_anme="ANS_{0}_{1}".format(img,os.getpid()), _path=__setting["_path"])
    else:
        __email = Email()
        __email.send_email(to=__setting["email_error"],file_name="{0}_{1}.png".format(img,os.getpid()),body="Error",subject="Error en pagina")
        print("Email de error enviado")

def screenshot(step_name):
    global __setting
    global __driver
    __driver.get_screenshot_as_file("{0}/out/{1}_{2}.png".format(__setting["_path"],step_name,os.getpid()))


def wait(sec=0,id=""):
    global __driver
    try:
        intent = 0
        while intent < 3:
            __driver.implicitly_wait(sec)
            print("intento",intent)
            try:
                print("Esperando elemento ", id, __driver.current_url)
                elem = __driver.find_element_by_id(id)
                if elem:
                    return True
                else:
                    __driver.implicitly_wait(sec)
            except  Exception as ex:
                print("Er",ex)
            intent +=1
    except Exception as ex:
        print("Error en Wait", ex)
    return False

def search_error():
    global __driver
    try:
        e = __driver.find_element_by_id("form1")
        if "error_page" in e.get_property("action"):
            print("Error in page")
            return True
        else:
            print("Step Good")
            return False
    except:
        return False

