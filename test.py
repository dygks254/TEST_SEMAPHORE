import json, os,sys
import click

file_path = os.path.dirname(os.path.realpath(__file__))

def add():
  print("aaaa")
  tmp = { '/home/yohan/PROJECT/Jenkins/TEST_SEMAPHORE/libs/slave_list/jobs1' : 5 }

  with open( f"{file_path}/build/slave_add/test3", 'w' ) as f:
    json.dump(tmp, f)


  tmp = { '/home/yohan/PROJECT/Jenkins/TEST_SEMAPHORE/libs/slave_list/jobs2' : 5 }

  with open( f"{file_path}/build/slave_add/test2", 'w' ) as f:
    json.dump(tmp, f)

def rm():
  tmp = { '/home/yohan/PROJECT/Jenkins/TEST_SEMAPHORE/libs/slave_list/jobs1' : 4 }

  with open( f"{file_path}/build/slave_rm/test3", 'w' ) as f:
    json.dump(tmp, f)


  tmp = { '/home/yohan/PROJECT/Jenkins/TEST_SEMAPHORE/libs/slave_list/jobs2' : 5 }

  with open( f"{file_path}/build/slave_rm/test2", 'w' ) as f:
    json.dump(tmp, f)


globals()[sys.argv[1]]()