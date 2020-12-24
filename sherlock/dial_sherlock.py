from subprocess import *
import os


def dial_sherlock(username: str):
    working_dir = os.path.dirname(os.path.realpath(__file__))
    out = Popen(["python3", "sherlock", username], cwd=working_dir, stdout=PIPE).communicate()[0]
    out = str(out.decode("ascii").replace("\\n", "").split("[+]")[1:]).split('\' ')[1:]
    modified = []
    for result in out:
        result = result.split("\\x")[0].split(": ")
        modified.append({result[0]: result[1]})
    print(modified)
    return modified
