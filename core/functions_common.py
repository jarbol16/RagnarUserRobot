import os
def remove_file(file_anme=None,_path=None):
    try:
        print("Borrando imagen {0}/out/{1}.png".format(_path,file_anme))
        os.remove("{0}/out/{1}.png".format(_path,file_anme))
    except:
        pass

