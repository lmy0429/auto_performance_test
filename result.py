import requests, jsonpath, json, os
from getpath import getpath


class Result():
    def __init__(self, project, jmx_script, start_time, end_time):
        self.result_list = ''
        self.result_dic = {}
        self.api_name_list = ''
        self.test_result = {}
        self.api_result_dic = {}
        self.project = project
        self.jmx_script = jmx_script
        self.start_time = start_time
        self.end_time = end_time

    def testresultdata(self, path):
        file_list = os.listdir(path)
        for file_name in file_list:
            if file_name.endswith("csv"):
                with open(path + os.path.sep + file_name, 'r', encoding='utf-8')as f:
                    data = f.readlines()
                    data_title = data[0].replace("\n", "").split(",")
                    data.pop(0)
                    result_list = []
                    for row_data in data:
                        data_dic = dict(zip(data_title, row_data.split(",")))
                        result_list.append(data_dic)
        return result_list

    def label(self, data):
        return data.get('label')

    def set_result_dic(self):
        self.result_list = self.testresultdata(
            getpath(self.project).get("result_csv") + os.path.sep + self.jmx_script[:-4])
        self.result_list.sort(key=self.label)
        result_list_copy = self.result_list
        api_name = [i.get("label") for i in self.result_list]
        self.api_name_list = list(set(api_name))
        self.api_name_list.sort()
        for i in range(len(self.api_name_list)):
            values = []
            for j in range(len(result_list_copy)):
                if self.api_name_list[i] not in self.result_dic:
                    values.append(result_list_copy[0])
                    self.result_dic[self.api_name_list[i]] = values
                    result_list_copy.pop(0)
                    continue
                if self.api_name_list[i] == result_list_copy[0].get("label"):
                    values.append(result_list_copy[0])
                    self.result_dic[self.api_name_list[i]] = values
                    result_list_copy.pop(0)
                else:
                    break

    def merge_restul(self):
        self.set_result_dic()
        cpu_rate_list = self.get_grafana_result("cpu")
        cpu_rate_avg = sum(cpu_rate_list) / len(cpu_rate_list)
        for apiname in self.api_name_list:
            self.api_result_dic = {}
            self.avg_time_result(apiname)
            self.tps_result(apiname)
            self.success_result(apiname)
            self.api_result_dic["CPU_RATE"] = cpu_rate_avg
            self.test_result[apiname] = self.api_result_dic
        print(self.test_result)
        return self.test_result

    def tps_result(self, apiname):
        timeStamp_list = [int(single_result.get("timeStamp")) for single_result in self.result_dic.get(apiname)]
        if len(timeStamp_list) == 1:
            tps = 1 / int(self.result_dic.get(apiname)[0].get("elapsed"))
        else:
            total_time = max(timeStamp_list) - min(timeStamp_list)
            tps = len(timeStamp_list) / total_time * 1000
        self.api_result_dic["TPS"] = tps
        return self.api_result_dic

    def success_result(self, apiname):
        success_result_list = [result.get('success') for result in self.result_dic.get(apiname)]
        error_count = success_result_list.count("false")
        self.api_result_dic["Error"] = error_count

    def avg_time_result(self, apiname):
        time_list = [time.get("elapsed") for time in self.result_dic.get(apiname)]
        sum_time = 0
        for time in time_list:
            sum_time += int(time)
        avg_time = sum_time / len(time_list)
        self.api_result_dic["AVG_TIME"] = avg_time

    def get_grafana_result(self, rate_name):
        # config_path = "project.{0}.config".format(self.project)
        # config = __import__(config_path)
        # rate_name_url = getattr(config, rate_name)
        config_path = getpath(self.project).get("config_path")
        with open(config_path, "r", encoding='utf-8')as f:
            config = json.load(f)
        rate_name_url = config.get(rate_name)
        header = config.get("grafana_header")
        response = requests.get(rate_name_url.format(self.start_time, self.end_time), headers=header)
        print("{}查询结果：".format(rate_name) + response.content.decode("utf-8"))
        rate_list = [float(x[1]) for x in jsonpath.jsonpath(json.loads(response.content), 'data.result[0].values')[0]]
        return rate_list
