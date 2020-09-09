import os


def getpath(project):
    path = {}
    base_path = os.path.dirname(os.path.abspath(__file__))
    path["base"] = base_path
    path["jmx_script_path"] = base_path + "/project/{0}/script".format(project)
    path["config_path"] = base_path + "/project/{0}/config.json".format(project)
    path["result_csv"] = base_path + "/data/result/{0}".format(project)
    return path
