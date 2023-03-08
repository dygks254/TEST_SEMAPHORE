import argparse
import subprocess
import json
import sys, os, shutil, re
import time


class Configuration():
  configuration : dict

  def __init__(self) -> None:
    return self.configuration
  
  @classmethod
  def update(self, data:dict):
    self.configuration = data
    return data

def parser():
  parse = argparse.ArgumentParser("Start semaphore host")
  parse.add_argument("--source", type=argparse.FileType('r'), help="Source file path")
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
      else:
        if tmp_key in Configuration.configuration['slave_list'].keys():
          Configuration.configuration['slave_list'][tmp_key] = Configuration.configuration['slave_list'][tmp_key] - tmp_qnum[tmp_key]
    os.remove(tmp_path)
  
  update_json(file=source_data['q_file'], buf_configuration=Configuration.configuration)
  # with open(sema_data['q_file'], 'w') as f_q:
    
    
    


def main( args : parser, source_data : dict ):
  
  for each in [ source_data['build_path'], source_data['add_list'], source_data['rm_list']]:
    make_tree(each)
  
  write_file(file_path=source_data['r_file'], text="TRUE")
  write_file(file_path=source_data['status'], text="BLOCK")
    
    
  Configuration.update( data= update_json(file=source_data['q_file'], buf_configuration={
     'total_q' : source_data['total_q']
    ,'running_q' : args.running
    ,'slave_list' : {}
  }))
  
  print(Configuration.configuration)
  
  running_status = "TRUE"
  while( running_status != "FALSE" ):
    time.sleep(3)
    write_file(file_path=source_data['status'], text="BLOCK")
    update_list(args=args, source_data=source_data, type="add")
    update_list(args=args, source_data=source_data, type="rm")
    with open(source_data['r_file'], 'r') as f_status:
      running_status =  re.findall(r'\w+', f_status.readline())[0]
      print(running_status)
    
    write_file(file_path=source_data['status'], text="OPEN")
    
if __name__=="__main__":
  args = parser().parse_args()
  source_data = json.loads(args.source.read())
  main( args=args, source_data=source_data )
  
  
    