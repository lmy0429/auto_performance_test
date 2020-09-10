import requests, jsonpath, json, os, time
from config import getpath
from sqlite_utils import Database
from . import config


class Result():
    def __init__(self, project, jmx_script, start_time, end_time):
        self.result_list = ''
        self.result_dic = {}
        self.api_name_list = ''
        self.test_result = {}
        self.project = project
        self.jmx_script=jmx_script
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
                        data_dic["start_time"] = time.strftime("%Y-%m-%d %X")
                        csv_data.append(data_dic)
        db = Database(config.db)
        db["csv_data"].insert_all(csv_data, hash_id="id")

    def set_result_data(self, path):
        cpu_rate_list = self.get_grafana_result("cpu")
        cpu_rate_avg = self.avg(cpu_rate_list)
        # memory_rate_list = self.get_grafana_result("memory")
        # memory_rate_avg = self.avg(memory_rate_list)
        with open(path + os.path.sep + "statistics.json", "r", encoding="utf-8")as f:
            data = json.load(f)
        data_dic = json.loads(data)
        sample_list = data_dic.keys()
        data_dic["project"] = self.project
        data_dic["start_time"] = time.strftime("%Y-%m-%d %X")
        for sample in sample_list:
            data_dic[sample]["cpu"] = cpu_rate_avg
            # data_dic[sample]["memory"] = memory_rate_avg
        db = Database(config.db)
        db["test_result"].insert(data_dic, hash_id="id")
        self.test_result = data_dic
        return self.test_result

    def get_grafana_result(self, rate_name):
        config_path = getpath(self.project).get("config_path")
        with open(config_path, "r", encoding='utf-8')as f:
            config = json.load(f)
        rate_name_url = config.get(rate_name)
        header = config.get("grafana_header")
        response = requests.get(rate_name_url.format(self.start_time, self.end_time), headers=header)
        print("{}查询结果：".format(rate_name) + response.content.decode("utf-8"))
        rate_list = [float(x[1]) for x in jsonpath.jsonpath(json.loads(response.content), 'data.result[0].values')[0]]
        return rate_list

    def avg(self, data_list):
        avg = sum(data_list) / len(data_list)
        return avg
