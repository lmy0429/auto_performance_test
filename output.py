from config import getpath
import time
from string import Template


def result_out(project, jmx_script, test_result):
    output_path = getpath(project).get("result_csv")
    with open("{0}/{1}/{1}_{2}.csv".format(output_path, jmx_script[:-4], time.strftime("%Y%m%d%H%M%S")), "a")as f:
        f.write(
            "transaction,sampleCount,errorCount,errorPct,meanResTime,minResTime,maxResTime,90%ResTime,95%ResTime,"
            "99%ResTime,throughput,CPU,memory,receivedKBytesPerSec,sentKBytesPerSec\n")
        del test_result["project"]
        del test_result["scenario"]
        del test_result["start_time"]
        del test_result["threads_num"]
        del test_result["loops"]
        for apiname in test_result.keys():
            row_data = Template(template).safe_substitute(
                transaction=test_result[apiname]["transaction"],
                sampleCount=str(test_result[apiname]["sampleCount"]),
                errorCount=str(test_result[apiname]["errorCount"]),
                errorPct=str(test_result[apiname]["errorPct"]),
                meanResTime=str(test_result[apiname]["meanResTime"]),
                minResTime=str(test_result[apiname]["minResTime"]),
                maxResTime=str(test_result[apiname]["maxResTime"]),
                pct1ResTime=str(test_result[apiname]["pct1ResTime"]),
                pct2ResTime=str(test_result[apiname]["pct2ResTime"]),
                pct3ResTime=str(test_result[apiname]["pct3ResTime"]),
                throughput=str(test_result[apiname]["throughput"]),
                CPU=str(test_result[apiname]["cpu"]),
                memory="",
                receivedKBytesPerSec=str(test_result[apiname]["receivedKBytesPerSec"]),
                sentKBytesPerSec=str(test_result[apiname]["sentKBytesPerSec"])
            )
            f.write(row_data)
    print("success")


template = "$transaction,$sampleCount,$errorCount,$errorPct,$meanResTime,$minResTime,$maxResTime,$pct1ResTime," \
           "$pct2ResTime,$pct3ResTime,$throughput, $CPU,$memory,$receivedKBytesPerSec,$sentKBytesPerSec\n"
