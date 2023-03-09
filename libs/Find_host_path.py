import argparse, os, re

def parser():
  parse = argparse.ArgumentParser("Start semaphore host")
  parse.add_argument("--host", type=str, help="Host job name")
  parse.add_argument("--workspace", type=str, help="Workspace path")
  parse.add_argument("--job_name", type=str, help="Jenkins job name")
  return parse

def main(args : parser):
  jenkins_workspcae = re.sub(f"{args.job_name}.*", "", args.workspace )
  buf_host_path = ""
  for each in (list((args.host).split("/")))[:-1]:
    buf_host_path += each
  host_workspace = jenkins_workspcae + buf_host_path
  
  while(True):
    for each in os.listdir(host_workspace):
      tmp_path = host_workspace + each + "/build/running.txt"
      if os.path.isfile(tmp_path):
        with open(tmp_path, 'r') as f_running:
          if "TRUE" in f_running.read():
            print(host_workspace + each)
            return 0
  
if __name__=="__main__":
  args = parser().parse_args()
  main(args = args)
  
   