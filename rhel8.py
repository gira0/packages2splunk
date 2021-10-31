#!/bin/python3

import dnf
import requests
import platform
   
base = dnf.Base()
base.fill_sack()

q = base.sack.query()
i = q.installed()
print(i)

packages = list(i)  # i only gets evaluated here
payload = list()

for pkg in packages:
    pack = '{{"event":"{0},{1},{2}"}}'.format(pkg.name,pkg.evr,pkg.reponame)
    payload.append(pack)


joined_payload = "".join(payload)

token = "Splunk 5cdd032e-fdf5-4792-89fd-172fb5a333b8"
header = {'content-type': 'application/json','Authorization': token}

url = "https://10.16.0.1:8088/services/collector?sourcetype=csv&host={0}".format(platform.node())
r = requests.post(url, data=joined_payload, headers=header, verify=False)

