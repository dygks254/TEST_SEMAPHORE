import json
import os

file_path = os.path.dirname(os.path.realpath(__file__))


tmp = { 'test1' : 5 }

with open( f"{file_path}/build/slave_add/test3", 'w' ) as f:
  json.dump(tmp, f)


tmp = { 'test2' : 5 }

with open( f"{file_path}/build/slave_add/test2", 'w' ) as f:
  json.dump(tmp, f)


tmp = { 'test1' : 4 }

with open( f"{file_path}/build/slave_rm/test3", 'w' ) as f:
  json.dump(tmp, f)


tmp = { 'test2' : 5 }

with open( f"{file_path}/build/slave_rm/test2", 'w' ) as f:
  json.dump(tmp, f)