import subprocess

def dynamic_check_output(command):
    result = ""
    print(command)
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE)

    for b_line in iter(process.stdout.readline, b''):
        try:
            line = b_line.decode("cp949")
        except:
            try:
                line = b_line.decode("utf-8")
            except:
                pass

        print(line, end="")
        result += line

    return result