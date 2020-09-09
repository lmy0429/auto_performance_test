import requests, jsonpath, json
from getpath import getpath


class DATA():
    def __init__(self, project, start_time, end_time):
        self.result_list = ''
        self.result_dic = {}
        self.api_name_list = ''
        self.test_result = {}
        self.api_result_dic = {}
        self.project = project
        self.start_time = start_time
        self.end_time = end_time

    def testresultdata(self, path):
        with open(path, 'r', encoding='utf-8')as f:
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
        self.result_list = self.testresultdata(getpath(self.project).get("result_csv"))
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
        return self.result_dic

    def merge_restul(self):
        cpu_rate_list = self.get_grafana_result("cpu")
        cpu_rate_avg = sum(cpu_rate_list) / len(cpu_rate_list)
        for apiname in self.api_name_list:
            self.avg_time_result(apiname)
            self.tps_result(apiname)
            self.success_result(apiname)
            self.test_result[apiname] = self.api_result_dic
            self.api_result_dic["CPU_RATE"] = cpu_rate_avg
        print(self.test_result)
        return self.test_result

    def tps_result(self, apiname):
        self.api_result_dic = {}
        timeStamp_list = [int(single_result.get("timeStamp")) for single_result in self.result_dic.get(apiname)]
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
        config = __import__(self.project)
        rate_name_url = getattr(config, rate_name)
        header = getattr(config, "grafana_header")
        response = requests.get(rate_name_url.format(self.start_time, self.end_time), headers=header)
        print("{}查询结果：".format(rate_name) + response.content)
        rate_list = [float(x[1]) for x in jsonpath.jsonpath(json.loads(response.content), 'data.result[0].values')[0]]
        return rate_list

    def result_out(self):
        test_result = self.merge_restul()
        with open("testresult.csv", "a")as f:
            f.write("API_NAME,TPS,CPU_RATE\n")
            for apiname in test_result.keys():
                f.write("{0},{1},{2}\n".format(apiname, test_result[apiname]["TPS"],
                                               test_result[apiname]["CPU_RATE"]))
        print("success")
