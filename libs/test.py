import json
import os

file_path = os.path.dirname(os.path.realpath(__file__))
  
import json, os,sys

def add():
  print("aaaa")
  tmp = { f"{file_path}/../build_slave1" : 20 }

  with open( f"{file_path}/../build/slave_add/test3", 'w' ) as f:
    json.dump(tmp, f)


  tmp = { f"{file_path}/../build_slave2" : 30 }

  with open( f"{file_path}/../build/slave_add/test2", 'w' ) as f:
    json.dump(tmp, f)

def rm():
  tmp = { f"{file_path}/../build_slave1" : 4 }

  with open( f"{file_path}/../build/slave_rm/test3", 'w' ) as f:
    json.dump(tmp, f)


  tmp = { f"{file_path}/../build_slave2" : 5 }

  # with open( f"{file_path}/../build/slave_rm/test2", 'w' ) as f:
  #   json.dump(tmp, f)


globals()[sys.argv[1]]()