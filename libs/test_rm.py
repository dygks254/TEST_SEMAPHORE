import json


tmp = { 'test1' : 5 }

with open( "/home/yohan/PROJECT/Jenkins/TEST_SEMAPHORE/libs/build/slave_rm/test3", 'w' ) as f:
  json.dump(tmp, f)
  
  
tmp = { 'test2' : 5 }

with open( "/home/yohan/PROJECT/Jenkins/TEST_SEMAPHORE/libs/build/slave_rm/test2", 'w' ) as f:
  json.dump(tmp, f)