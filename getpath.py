import os


def getpath(project):
    path = {}
    path["jmx_script_path"] = "./project/{0}/script".format(project)
    path["config_path"] = "./project/{0}/config.py".format(project)
    path["result_csv"]="./data/result/{0}".format(project)
    return path
