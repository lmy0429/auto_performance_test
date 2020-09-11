import requests, jsonpath, json, os, time
from config import getpath
from sqlite_utils import Database
import config


class Result():
    def __init__(self, project, jmx_script, start_time, end_time):
        self.result_list = ''
        self.result_dic = {}
        self.api_name_list = ''
        self.test_result = {}
        self.project = project
        self.jmx_script = jmx_script
        self.start_time = start_time
        self.end_time = end_time

    def set_csv_data(self, path):
        file_list = os.listdir(path)
        for file_name in file_list:
            if file_name.endswith("csv"):
                with open(path + os.path.sep + file_name, 'r', encoding='utf-8')as f:
                    data = f.readlines()
                    data_title = data[0].replace("\n", "").split(",")
                    data.pop(0)
                    csv_data = []
                    for row_data in data:
                        data_dic = dict(zip(data_title, row_data.split(",")))
                        data_dic["project"] = self.project
                        data_dic["start_time"] = time.strftime("%Y-%m-%d %X", time.localtime(self.start_time))
                        csv_data.append(data_dic)
        db = Database(config.db)
        db["csv_data"].insert_all(csv_data, hash_id="id")

    def set_result_data(self, path, threads_num, loops):
        cpu_rate_list = self.get_grafana_result("cpu")
        cpu_rate_avg = self.cpu_avg(cpu_rate_list)
        memory_rate_list = self.get_grafana_result("memory")
        memory_rate_avg = self.memory_avg(memory_rate_list)
        with open(path + os.path.sep + "statistics.json", "r", encoding="utf-8")as f:
            data_dic = json.load(f)
        sample_list = data_dic.keys()
        for sample in sample_list:
            data_dic[sample]["cpu"] = cpu_rate_avg
            data_dic[sample]["memory"] = memory_rate_avg
        str_start_time = time.strftime("%Y-%m-%d %X", time.localtime(self.start_time))
        db = Database(config.db)
        db["test_result"].insert({
            "project": self.project,
            "scenario": self.jmx_script[:-4].replace("tmp", ""),
            "threads_num": threads_num,
            "loops": loops,
            "start_time": str_start_time,
            "result": data_dic},
            hash_id="id")
        data_dic["project"] = self.project
        data_dic["scenario"] = self.jmx_script[:-4].replace("tmp", "")
        data_dic["start_time"] = str_start_time
        data_dic["threads_num"] = threads_num
        data_dic["loops"] = loops
        self.test_result = data_dic
        return self.test_result

    def get_project_config(self):
        try:
            config_path = getpath(self.project).get("config_path")
            with open(config_path, "r", encoding='utf-8')as f:
                project_config = json.load(f)
            return project_config
        except:
            print("请在项目配置文件（config.json）中设置grafana配置")

    def get_grafana_result(self, rate_name):
        project_config = self.get_project_config()
        rate_name_url = project_config.get(rate_name)
        header = project_config.get("grafana_header")
        response = requests.get(rate_name_url.format(self.start_time, self.end_time), headers=header)
        print("{}查询结果：".format(rate_name) + response.content.decode("utf-8"))
        rate_list = [float(x[1]) for x in jsonpath.jsonpath(json.loads(response.content), 'data.result[0].values')[0]]
        return rate_list

    def cpu_avg(self, data_list):
        avg = sum(data_list) / len(data_list)
        return avg

    def memory_avg(self, data_list):
        project_config = self.get_project_config()
        avg = sum(data_list) / (1024 * 1024 * 1024 * project_config.get("memory_total") * len(data_list))
        return avg
