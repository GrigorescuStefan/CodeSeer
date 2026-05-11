import subprocess

def build_command(user_input):
    return f"ping -c 1 {user_input}"

def run():
    target = input("Target IP: ")
    cmd = build_command(target)
    subprocess.call(cmd, shell=True)

run()