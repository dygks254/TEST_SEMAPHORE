import argparse
import json
import os, shutil, re
import time
import copy

class Configuration():
  configuration : dict

  def __init__(self) -> None:
    return self.configuration

  @classmethod
  def update(self, data:dict):
    self.configuration = data
    return data

  @classmethod
  def data(self):
    return copy.deepcopy(self.configuration)

def parser():
  parse = argparse.ArgumentParser("Start semaphore host")
  parse.add_argument("--source", type=argparse.FileType('r'), default=None, help="Source file path")
  parse.add_argument("--running", type=int, default=0, help="Source file path")
  return parse

def make_tree(tree_path):
  try:
    if os.path.exists(tree_path):
      shutil.rmtree(tree_path)
    os.makedirs(tree_path)
    print(f"Success make tree :: {tree_path}")
  except:
    print(f"Failed make tree :: {tree_path}")
    exit(1)
  return True

def update_json(file : str, buf_configuration : dict):
  if os.path.isfile(file):
    with open(file, 'r' ) as f_json:
      tmp_json = json.loads(f_json.read())
  else:
    tmp_json = {}
  for key, value in buf_configuration.items():
    tmp_json[key] = value
  with open(file, 'w') as f_json:
    json.dump(tmp_json, f_json, indent=4)
  return tmp_json

def write_file( file_path : str, text : str):
  with open(file_path, 'w') as f_running:
    f_running.write(text)

def update_list(args : parser, source_data : dict, type : str):
  filenames = next(os.walk( source_data[f"{type}_list"] ), (None, None, []))[2]

  for each in filenames:
    tmp_path = os.path.join(source_data[f"{type}_list"], each)

    with open( tmp_path , 'r' ) as f_up:
      tmp_qnum =  json.loads(f_up.read())
      tmp_key = list(tmp_qnum.keys())[0]
      if type == "add":
        if tmp_key not in Configuration.configuration['slave_list'].keys():
          Configuration.configuration['slave_list'][tmp_key] = tmp_qnum[tmp_key]
          Configuration.configuration['dis_semaphore'][tmp_key] = 0
      else:
          Configuration.configuration['running_q'] -= tmp_qnum[tmp_key]
          Configuration.configuration['dis_semaphore'][tmp_key] -= tmp_qnum[tmp_key]
    os.remove(tmp_path)

  update_json(file=source_data['q_file'], buf_configuration=Configuration.configuration)


def distribute_sem( args : parser, source_data: dict):

  if Configuration.configuration['total_q'] - Configuration.configuration['running_q'] <= 0:
    return

  tmp_dict = Configuration.data()

  for key, value in Configuration.configuration['slave_list'].items():
    print(f"{key} : {value} ")
    key_file = f"{key}/semaphore_reg"
    if not os.path.isfile(key_file) :
      av_q =  tmp_dict['total_q'] - tmp_dict['running_q']
      if av_q >= value:
        trans_q = value
        tmp_dict['slave_list'].pop(key)
      else:
        trans_q = av_q
        tmp_dict['slave_list'][key] = value - av_q
      tmp_dict['dis_semaphore'][key] += trans_q
      tmp_dict['running_q'] += trans_q
      with open(key_file, 'w') as f_reg:
        json.dump([trans_q], f_reg, indent=2)

    else:
      print(f"--- file exist {key_file}")

  Configuration.configuration.update(tmp_dict)
  update_json(file=source_data['q_file'], buf_configuration=Configuration.configuration)


def main( args : parser, source_data : dict ):

  for each in [ source_data['build_path'], source_data['add_list'], source_data['rm_list']]:
    make_tree(each)

  write_file(file_path=source_data['r_file'], text="TRUE")
  write_file(file_path=source_data['status'], text="BLOCK")


  Configuration.update( data= update_json(file=source_data['q_file'], buf_configuration={
     'total_q' : source_data['total_q']
    ,'running_q' : args.running
    ,'slave_list' : {}
    ,'dis_semaphore' : {}
  }))

  print(Configuration.configuration)

  running_status = "TRUE"
  while( running_status != "FALSE" ):
    time.sleep(2)
    write_file(file_path=source_data['status'], text="BLOCK")
    time.sleep(1)
    update_list(args=args, source_data=source_data, type="add")
    update_list(args=args, source_data=source_data, type="rm")
    with open(source_data['r_file'], 'r') as f_status:
      running_status =  re.findall(r'\w+', f_status.readline())[0]
      if running_status == "FALSE":
        print("Host semahore Done")
        return 0

    distribute_sem(args=args, source_data=source_data)

    write_file(file_path=source_data['status'], text="OPEN")

if __name__=="__main__":
  args = parser().parse_args()

  if args.source == None:
    from pathlib import Path
    top_path = Path(os.path.dirname(os.path.realpath(__file__))).parent
    source_data = {
      "build_path": f"{top_path}/build",
      "q_file": f"{top_path}/build/semaphore_q.json",
      "total_q": 10,
      "r_file": f"{top_path}/build/running.txt",
      "add_list": f"{top_path}/build/slave_add",
      "rm_list": f"{top_path}/build/slave_rm",
      "status": f"{top_path}/build/status.txt"
    }
  else :
    source_data = json.loads(args.source.read())
  main( args=args, source_data=source_data )

