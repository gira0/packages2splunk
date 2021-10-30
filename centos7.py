#!/bin/pythyon

import subprocess
import requests
import platform

data = subprocess.Popen(["repoquery", "--installed","*","--queryformat=\'%{name} %{evr} %{ui_from_repo}\'"], stdout=subprocess.PIPE).communicate()[0]

payload = list()
for line in data.replace("'","").splitlines():
    pkg_data = line.split()
    #if pkg_data[0] == "zip" or pkg_data[0] == "yum":
    pack = '{{"event":"{0},{1},{2}"}}'.format(pkg_data[0],pkg_data[1],pkg_data[2])
    
    payload.append(pack)

joined_payload = "".join(payload)

token = "Splunk 5cdd032e-fdf5-4792-89fd-172fb5a333b8"
header = {'content-type': 'application/json','Authorization': token}
#metadata = '{{"host":"{0}","sourcetype":"csv",{1}}}'.format(platform.node(),joined_payload)


url = "https://localhost:8088/services/collector?sourcetype=csv&host={0}".format(platform.node())
r = requests.post(url, data=joined_payload, headers=header, verify=False)
# print(vars(r))
# print(joined_payload)
