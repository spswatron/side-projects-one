from subprocess import *
import os


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
