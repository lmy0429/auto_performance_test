##概述
    通过命令行运行后，会自动根据输入项目名称、并发数、循环次数执行性能测试，执行完成后自动从grafana拉取执行期间服务器
    资源状态（当前仅支持CPU、内存），并输出csv结果文件（./data/result/[project]/[jmx name]/*.csv），主要解决了以下问题：
    1.不同并发脚本压测，每次需要手动修改脚本；
    2.压测期间服务器CPU、内存占用数据需人为统计计算，且详细数据不易拿到；
    3.压测结果数据无统一存放、记录；
    4.不易部署CI。
##脚本
    脚本设置遵循原则：
    1.一个场景一个脚本；
    2.脚本中“LoopController.loops”和“ThreadGroup.num_threads”值分别设置为“$loops”、“$threads_num”；
    3.建议脚本名称保持与脚本内线程组名称一致。
##Project
    创建项目名称目录，存放脚本（script/*.jmx）和项目配置（config.json）
##RUN
    python run.py -p [project name] -t [threads num] -l [loops]
    目前单次运行会执行脚本存放目录下所有脚本
##Result&Report
    执行结果在下一次同脚本执行时自动删除上次执行结果文件