import os
from string import Template
import getpath


class Script():

    def __init__(self, project):
        self.project = project
        self.path = getpath.getpath(project)
        self.jmx_script_path = self.path["jmx_script_path"]

    def jmeter_run(self, jmx_script):
        excute_jmx_script = self.jmx_script_path + os.path.sep + jmx_script
        os.mkdir(self.path["base"] + "/data/result/{0}".format(self.project))
        os.mkdir(self.path["base"] + "/data/report/{0}".format(self.project))
        result_path = self.path["base"] + "/data/result/{0}".format(self.project)
        os.mkdir(result_path + "/{0}".format(jmx_script[:-4]))
        report_path = (self.path["base"] + "/data/report/{0}/{1}".format(self.project, jmx_script[:-4]))
        command = 'D:/apache-jmeter-5.1.1/bin/jmeter.bat -n -t {0} -l {1}/{2}/{2}.csv -j {1}/{2}/{2}log -e -o {3} &'.format(
            excute_jmx_script, result_path, jmx_script[:-4], report_path)
        os.system(command)
        os.remove(excute_jmx_script)

    def build_jmx(self, threads_num, loops):
        file_list = os.listdir(self.jmx_script_path)
        excute_jmx_script_list = []
        for file_name in file_list:
            if file_name.endswith("jmx"):
                with open(self.jmx_script_path + os.path.sep + file_name, "r", encoding="utf-8") as file:
                    tmpstr = Template(file.read()).safe_substitute(
                        threads_num=threads_num,
                        loops=loops
                    )
                with open(self.jmx_script_path + os.path.sep + "tmp" + file_name, "w+", encoding="utf-8") as file:
                    file.writelines(tmpstr)
                excute_jmx_script_list.append("tmp" + file_name)
        return excute_jmx_script_list
