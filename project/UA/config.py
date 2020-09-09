grafana_baseurl='http://grafana-bz-openshift-monitoring-sit.app.cloud.bz/api/datasources/proxy/2/api/v1/query_range'
cpu='http://grafana-bz-openshift-monitoring-sit.app.cloud.bz/api/datasources/proxy/2/api/v1/query_range?query=namespace_pod_name_container_name%3Acontainer_cpu_usage_seconds_total%3Asum_rate%7Bnamespace%3D%22uat%22%2Ccontainer_name!%3D%22POD%22%2Cpod_name%3D~%22ua-cn.*%22%7D&start={0}&end={1}&step=30'
grafana_header = {
    'Cookie': 'grafana_user=dev; 1de2e1d13cb333fdca3ade3a17fbe392=486ef57899a33e878fff510149bb9121; grafana_remember=1e81962d0dab345b398d602cf1b320407603bf9b22a122bb3f0408feadde31; grafana_sess=42dff4e72d24afe6'
}