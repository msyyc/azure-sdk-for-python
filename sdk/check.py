from pathlib import Path
from glob import glob
import re

candidates = [
    "compute/azure-mgmt-compute",
    "databox/azure-mgmt-databox",
    "resources/azure-mgmt-msi",
    "kubernetesconfiguration/azure-mgmt-kubernetesconfiguration",
    "eventhub/azure-mgmt-eventhub",
    "resources/azure-mgmt-resource",
    "keyvault/azure-mgmt-keyvault",
    "extendedlocation/azure-mgmt-extendedlocation",
    "resourcehealth/azure-mgmt-resourcehealth",
    "network/azure-mgmt-network",
    "databoxedge/azure-mgmt-databoxedge",
    "digitaltwins/azure-mgmt-digitaltwins",
    "storage/azure-mgmt-storage",
    "security/azure-mgmt-security",
    "network/azure-mgmt-dns",
    "redhatopenshift/azure-mgmt-redhatopenshift",
    "appconfiguration/azure-mgmt-appconfiguration",
    "appservice/azure-mgmt-web",
    "servicebus/azure-mgmt-servicebus",
    "applicationinsights/azure-mgmt-applicationinsights",
    "authorization/azure-mgmt-authorization",
    "containerregistry/azure-mgmt-containerregistry",
    "iothub/azure-mgmt-iothub",
    "appplatform/azure-mgmt-appplatform",
    "monitor/azure-mgmt-monitor",
    "edgeorder/azure-mgmt-edgeorder",
]

result = []
for item in candidates:
    folders = glob(f"{item}/**/_configuration.py", recursive=True)
    for f in folders:
         if "build" not in f and re.compile("v\d{4}_\d{2}_\d{2}").search(f):
            print(f"Found: {f}")
            with open(Path(f), "r") as file_in:
                content = file_in.readlines()
                if "self.api_version = api_version" not in "".join(content):
                    result.append(str(Path(f)))
    
if result:
    raise Exception("Found files that do not set api_version: \n" + "\n".join(result))