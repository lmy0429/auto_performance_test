import os, time
from string import Template
import getpath, shutil


class Script():

    def __init__(self, project):
        self.project = project
        self.jmx_script_path = getpath.getpath(self.project)["jmx_script_path"]

    def jmeter_run(self, jmx_script):
        excute_jmx_script = self.jmx_script_path + os.path.sep + "tmp" + jmx_script
        start_time = int(time.time())
        shutil.rmtree("./data/report/{0}".format(self.project))
        shutil.rmtree("./data/result/{0}".format(self.project))
        os.mkdir("./data/result/{0}".format(self.project))
        os.mkdir("./data/report/{0}".format(self.project))
        result_path = "./data/result/{0}".format(self.project)
        os.mkdir("./data/report/{0}/{1}".format(self.project, jmx_script[:-4]))
        report_path = ("./data/report/{0}/{1}".format(self.project, jmx_script[:-4]))
        command = 'jmeter -n -t {0} -l {1}/{3}.csv -j {2}/{3}log -e -o {4} &'.format(
            excute_jmx_script, result_path, report_path, jmx_script[:-4], report_path)
        os.system(command)
        end_time = int(time.time()) + 5000  # 增加5s以获取更准确的服务器监控数据
        os.remove(excute_jmx_script)
        return start_time, end_time

    def build_jmx(self, thread_num, loops):
        file_list = os.listdir(self.jmx_script_path)
        excute_jmx_script_list = []
        for file_name in file_list:
            if file_name.endswith("jmx"):
                with open(self.jmx_script_path + os.path.sep + file_name, "r", encoding="utf-8") as file:
                    tmpstr = Template(file.read()).safe_substitute(
                        num_threads=thread_num,
                        loops=loops
                    )
                with open(self.jmx_script_path + os.path.sep + "tmp" + file_name, "w+", encoding="utf-8") as file:
                    file.writelines(tmpstr)
                excute_jmx_script_list.append(self.jmx_script_path + os.path.sep + "tmp" + file_name)
        return excute_jmx_script_list
