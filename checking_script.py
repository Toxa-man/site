#!/usr/bin/python3.5

import cgi, cgitb, random, string, json, os
from subprocess import run, PIPE, Popen, STDOUT, TimeoutExpired
import xml.etree.ElementTree as ET

def check_code(return_code):
    if return_code == 0:
        return "success"
    elif return_code == 2:
        return "process_timeout"
    else:
        return "failed"

cgitb.enable()

print ("Content-Type: application/json, charset=utf-8\r\n\r\n")
#print ("Content-Type: text/html, charset=utf-8\r\n\r\n")
data = cgi.FieldStorage()

sourceCode = data['srcCode'].value
std_input = ""
if "input" in data:
    std_input = data["input"].value
# print("Std input: \"" + std_input + "\"")
fileName = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))
try:
    with open(fileName + ".cpp", encoding='utf-8', mode="w") as text_file:
        text_file.write(sourceCode)
except Exception as ex:
    print(type(ex).__name__ + ": " + ex.args)

build_args = ("g++", "-o", fileName, "-std=c++17", "-Wall", fileName + ".cpp")
proc_desc = Popen(build_args, stdout=PIPE, stderr=STDOUT)
compile_return_code = proc_desc.wait(2)
compile_output = proc_desc.stdout.read()
compile_output = compile_output.decode('utf-8').replace("\n", "<br>")
# print("return code: " + str(compile_return_code))
# print("compile output: " + compile_output)
# with open("/usr/lib/cgi-bin/wtf.txt", "w") as text_file:
#     text_file.write(compile_output)

valgrind_error_code = 1
valgrind_return_code = valgrind_error_code
errors_str = ''
if compile_return_code == 0:
    valgrind_args = ("valgrind", "--leak-check=full", "--xml=yes", "--error-exitcode=" + str(valgrind_error_code), "--xml-file=" + fileName + ".xml", "./" + fileName)
    try:
        valgrind_desc = run(valgrind_args, stdout=PIPE, stderr=STDOUT, input=std_input.encode(), timeout=3)
        valgrind_return_code = valgrind_desc.returncode

        exec_stdout = valgrind_desc.stdout

        tree = ET.parse(fileName + ".xml")
        root = tree.getroot()
        errorsList = []
        for error in root.findall("error"):
            if error.find("xwhat") is not None:
                errorsList.append(error.find("xwhat").find("text").text)

            if error.find("what") is not None:
                errorsList.append(error.find("what").text)
            
            if error.find("auxwhat") is not None:
                errorsList.append(error.find("auxwhat").text)


        errors_str = "<br>".join(errorsList)
    except TimeoutExpired as inst:
        errors_str = "Process timeout error. May be you forgot to remove blocking operations?"
        valgrind_return_code = 2

    
json_str = json.dumps([{"build_result" : check_code(compile_return_code), "build_log" : compile_output},
                        {"valgrind_result" : check_code(valgrind_return_code), "valgrind_log" : errors_str} ])

print(json_str)
os.system("rm -f " + fileName + "*")
