import argparse, time
from jmeter import Script
from result import Result
from output import result_out

# ap = argparse.ArgumentParser()
# ap.add_argument("-p", "--project", required=True, help="project name")
# ap.add_argument("-t", "--threads_num", required=True, help="ThreadGroup threads num")
# ap.add_argument("-l", "--loops", required=True, help="ThreadGroup loop num")
# args = vars(ap.parse_args())


def run(project, threads_num, loops):
    jmeter = Script(project)
    excute_jmx_script_list = jmeter.build_jmx(threads_num, loops)
    for jmx_script in excute_jmx_script_list:
        start_time = int(time.time())
        jmeter.jmeter_run(jmx_script)
        end_time = int(time.time())+ 5000  # 增加5s以获取更准确的服务器监控数据
        result = Result(project, jmx_script,start_time, end_time)
        test_result = result.merge_restul()
        result_out(project, test_result)


# project = args["project"]
# threads_num = args["threads_num"]
# loops = args["loops"]
project="UA"
threads_num = 1
loops = 1
run(project, threads_num, loops)
