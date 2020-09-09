from getpath import getpath
import time


def result_out(project, test_result):
    output_path = getpath(project).get("result_csv")
    with open("{0}/{1}.csv".format(output_path, time.strftime("%Y%m%d%H%M%S")), "a")as f:
        f.write("API_NAME,AVG_TIME,Error,TPS,CPU_RATE\n")
        for apiname in test_result.keys():
            f.write("{0},{1},{2}\n".format(apiname, test_result[apiname]["TPS"],
                                           test_result[apiname]["CPU_RATE"]))
    print("success")
