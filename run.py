import argparse, time
from jmeter import Script
from result import Result
from output import result_out

ap = argparse.ArgumentParser()
ap.add_argument("-p", "-project", required=True, help="project name")
ap.add_argument("-t", "-thread_num", required=True, help="ThreadGroup threads num")
ap.add_argument("-l", "-loops", required=True, help="ThreadGroup loop num")
args = vars(ap.parse_args())


def run():
    project = args["project"]
    thread_num = args["thread_num"]
    loops = args["loops"]
    start_time = int(time.time())
    jmeter = Script(project)
    excute_jmx_script_list = jmeter.build_jmx(thread_num, loops)
    for jmx_script in excute_jmx_script_list:
        jmeter.jmeter_run(jmx_script)
    end_time = int(time.time())
    result = Result(project, start_time, end_time)
    test_result = result.merge_restul()
    result_out(project, test_result)


if __name__ == "__main__":
    run()
