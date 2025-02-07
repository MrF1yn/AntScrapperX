import subprocess


def run_script(script_name):
    process = subprocess.Popen(['python', script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in process.stdout:
        print(line.strip())
    for line in process.stderr:
        print(line.strip())
    process.wait()


run_script('Dependencies.py')
run_script('EnvDriverBot.py')
