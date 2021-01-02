from subprocess import *
import os

from sherlock.notify import QueryNotifyPrint
from sherlock.sherlock import sherlock
from sherlock.sites import SitesInformation


def dial_sherlock(username: str):
    python = os.path.dirname(os.path.realpath(__file__)) + "/venv" + "/bin" + "/python"
    out = Popen(["python3", "sherlock", username], stdout=PIPE).communicate()[0]
    out = str(out.decode("ascii").replace("\\n", "").split("[+]")[1:]).split('\' ')[1:]
    modified = []
    for result in out:
        result = result.split("\\x")[0].split(": ")
        modified.append({result[0]: result[1]})
    # print(modified)
    return modified


def call_sherlock(username: str):
    sites = SitesInformation(os.path.join(os.path.dirname(__file__), 'sherlock/resources/data.json'))
    site_data_all = {}
    for site in sites:
        site_data_all[site.name] = site.information
    return sherlock(username,
                    site_data_all,
                    QueryNotifyPrint(result=None))

