# -*- coding: utf-8 -*-
'''
按照列表进行GPU的转码工作；
'''
import os
import logging
import subprocess
import time

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("trlog.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

plist = "list.txt"
droot = "/mnt"
pnum = 2

#tr_cmd = "ffmpeg -hwaccel cuvid -i source -c:v h264_nvenc -c:a aac -b:a 100k -b:v 720k  -profile baseline  -y target   -metadata title=YUNSHI_GPU"
tr_cmd = "ffmpeg  -hwaccel cuvid -i source -c:v h264_nvenc -c:a aac -b:a 100k -b:v 720k  -y target   -metadata title=YUNSHI_GPU &"

Datas = open(plist , 'r', encoding='utf_8').readlines()


for line in Datas:
    file = os.path.basename(line).strip("\n")
    path = os.path.dirname(line)

    dpath = droot+"/"+path
    if not os.path.exists(dpath): 
        os.makedirs(dpath)
    
    sf = (path+"/"+file).replace(" ", "\ ")
    tf = (droot + "/").replace(" ", "\ ") + (path+"/"+file.split(".")[0]+".mp4").replace(" ", "\ ")
    cmd = tr_cmd.replace("source", sf).replace("target", tf)
    #设置循环进行控制是否在合理的进程处理数量，每一秒钟判断一次，
    while True:
        command = "ps -ef|grep YUNSHI_GPU|grep -v grep|wc -l"
        ret = subprocess.getoutput(command)
        if int(ret) < pnum :
            break
        time.sleep(1)
    logger.info("system call start:  " + cmd)
    subprocess.call(cmd, shell=True)
    time.sleep(6)

