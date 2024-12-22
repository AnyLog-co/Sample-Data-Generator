group1 = []
group2 = []

ips = ["10.10.1.10", "10.10.1.31", "10.10.1.201", "10.10.1.211", "10.10.1.212","10.10.1.213", "10.10.1.214",
       "10.10.1.215", "10.10.1.216", "10.10.1.202", "10.10.1.206", "10.10.1.205", "10.10.1.203", "10.10.1.204",
          "10.10.1.32", "10.10.1.33"]

for ip in ips:
    content = f"syslog_ip = {ip}\nrule_name = blockchain get (master, query, publisher, operator) where ip = !syslog_ip bring [*][name]\nset msg rule !rule_name if ip=!syslog_ip then dbms=monitoring and table=syslog and  extend = ip and syslog=true"
    if ip == "10.10.1.201" or ips.index(ip) % 2 == 0:
        group1.append(content)
    elif ip == "10.10.1.202" or ips.index(ip) % 2 != 0:
        group2.append(content)


for content in group2:
    print(content, "\n")



