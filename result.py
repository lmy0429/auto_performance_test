import requests, jsonpath, json


class DATA():
    def __init__(self, project, start_time, end_time):
        self.result_list = ''
        self.result_dic = ''
        self.api_name_list = ''
        self.test_result = ''
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
        self.result_list = self.testresultdata("./result/test.csv")
        self.result_list.sort(key=self.label)
        result_list_copy = self.result_list
        api_name = [i.get("label") for i in self.result_list]
        self.api_name_list = list(set(api_name))
        self.api_name_list.sort()
        result_dic = {}
        for i in range(len(self.api_name_list)):
            values = []
            for j in range(len(result_list_copy)):
                if self.api_name_list[i] not in result_dic:
                    values.append(result_list_copy[0])
                    result_dic[self.api_name_list[i]] = values
                    result_list_copy.pop(0)
                    continue
                if self.api_name_list[i] == result_list_copy[0].get("label"):
                    values.append(result_list_copy[0])
                    result_dic[self.api_name_list[i]] = values
                    result_list_copy.pop(0)
                else:
                    break
        return result_dic

    def set_test_restul(self):
        test_result = {}
        api_dic = {}
        cpu_rate_list = self.get_grafanadata()
        cpu_rate_avg = sum(cpu_rate_list) / len(cpu_rate_list)
        api_dic["CPU_RATE"] = cpu_rate_avg
        for apiname in self.api_name_list:
            timeStamp_list = [int(single_result.get("timeStamp")) for single_result in self.result_dic.get(apiname)]
            print(timeStamp_list)
            total_time = max(timeStamp_list) - min(timeStamp_list)
            tps = len(timeStamp_list) / total_time * 1000
            print(tps)
            api_dic["TPS"] = tps
            test_result[apiname] = api_dic
            api_dic = api_dic.copy()
        print(test_result)
        return test_result

    def get_grafanadata(self):
        config = __import__(self.project)
        cpu_rate_url = getattr(config, "grafana_baseurl" + "grafana_cpuurl")
        header = getattr(config, "grafana_header")
        cpu_response = requests.get(cpu_rate_url.format(self.start_time, self.end_time), headers=header)
        print(cpu_response.content)
        cpu_rate_list = [float(x[1]) for x in jsonpath.jsonpath(json.loads(cpu_response.content),
                                                                'data.result[0].values')[0]]
        return cpu_rate_list

    def result_out(self):
        test_result = self.set_test_restul()
        with open("testresult.csv", "a")as f:
            f.write("API_NAME,TPS,CPU_RATE\n")
            for apiname in test_result.keys():
                f.write("{0},{1},{2}\n".format(apiname, test_result[apiname]["TPS"],
                                               test_result[apiname]["CPU_RATE"]))
        print("success")
