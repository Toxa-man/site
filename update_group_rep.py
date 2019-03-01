#!/usr/bin/python3.5

import os, subprocess, datetime, json, sys
from collections import OrderedDict
from shutil import copyfile

#CHANGE WITH NEW COURSE
course_lab_id = 4 
repo_name = "labWorks_8373_2019"



def print_log(s):
    with open("update_rep.log", mode="a+") as text_file:
        text_file.write('[' + str(datetime.datetime.now()) + '] | ' + s + '\n')

if not os.path.isdir(repo_name):
    git_args = ("git", "clone", "https://github.com/Toxa-man/" + repo_name)
    try:
        ret = subprocess.run(git_args, timeout=40)
        if ret.returncode != 0:
            print_log("Unable to clone repository: " + git_args[-1])
            sys.exit()
    except subprocess.TimeoutExpired as inst:
            print_log("Timeout error while cloning repository: " + git_args[-1])
            sys.exit()


os.chdir(repo_name)

git_args = ("git", "pull")
subprocess.run(git_args)

students_dic = OrderedDict()

for dirname in sorted(os.listdir(os.getcwd())):
    if os.path.isdir(dirname) and dirname != ".git":
        labs_done = []
        mark = ""
        fio = ""
        os.chdir(dirname)
        if os.path.isfile("fio.txt"):
	        with open("fio.txt", mode="r") as text_file:
		        fio = text_file.read().replace("\n", "")
        for i in range(1, course_lab_id + 1):
            if os.path.isdir("lab_" + str(i)):
                labs_done.append(i)
                if i == course_lab_id:
                    with open("lab_" + str(i) + "/"+ "mark.txt", mode="r") as text_file:
                        mark = text_file.read().replace("\n", "")

        os.chdir("../")
        students_dic[dirname] = {"labs" : labs_done, "course_mark" : mark, "fio" : fio}

json_obj = json.dumps(students_dic)
os.chdir("../")
output_file_name = "data.json"
with open(output_file_name, mode="w") as text_file:
    text_file.write(json_obj)
copyfile(output_file_name, "/var/www/html/" + output_file_name)

