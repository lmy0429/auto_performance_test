import os

base_path = os.path.dirname(os.path.abspath(__file__))
db = base_path + "/pt.db"


def getpath(project):
    path = {}
    path["base"] = base_path
    path["jmx_script_path"] = base_path + "/project/{0}/script".format(project)
    path["config_path"] = base_path + "/project/{0}/config.json".format(project)
    path["result_csv"] = base_path + "/data/result/{0}".format(project)
    path["report_path"] = base_path + "/data/report/{0}".format(project)
    return path
