import argparse, time, shutil
from jmeter import Script
from result import Result
from output import result_out
from config import getpath

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--project", required=True, help="project name")
ap.add_argument("-t", "--threads_num", required=True, help="ThreadGroup threads num")
ap.add_argument("-l", "--loops", required=True, help="ThreadGroup loop num")
args = vars(ap.parse_args())


def run(project, threads_num, loops):
    '''

    :param project: 项目名称，保持与project目录项目名称一致
    :param threads_num: 并发数
    :param loops: 循环次数
    :return:
    '''
    jmeter = Script(project)
    path = getpath(project)
    excute_jmx_script_list = jmeter.build_jmx(threads_num, loops)
    for jmx_script in excute_jmx_script_list:
        try:
            shutil.rmtree(path["base"] + "/data/report/{0}/{1}".format(project, jmx_script[3:-4]))
        except Exception:
            print("删除项目历史报告目录失败,目录不存在")
            pass
        try:
            shutil.rmtree(path["base"] + "/data/result/{0}/{1}".format(project, jmx_script[3:-4]))
        except Exception:
            print("删除项目历史结果目录失败，目录不存在")
            pass
        time.sleep(3)
        start_time = int(time.time())
        jmeter.jmeter_run(jmx_script)
        end_time = int(time.time()) + 5000  # 增加5s以获取更准确的服务器监控数据
        result = Result(project, jmx_script, start_time, end_time)
        result.set_csv_data(getpath(project).get("result_csv") + "/{0}".format(jmx_script[3:-4]))
        test_result = result.set_result_data(getpath(project).get("report_path") + "/{0}".format(jmx_script[3:-4]),
                                             threads_num, loops)
        result_out(project, jmx_script, test_result)


project = args["project"]
threads_num = args["threads_num"]
loops = args["loops"]
# project = "testproject"
# threads_num = 1
# loops = 1
run(project, threads_num, loops)
