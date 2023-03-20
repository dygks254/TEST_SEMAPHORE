import groovy.json.*
import java.io.File

tmp_command = []
semaphore_file_name = ""
host_path = ""
def now_q_lengh = 0

class AV_semaphore{
  int av_semaphore2 = 0
  void updatenumber(int number){
    av_semaphore2 += number
  }
  int get_sem(){
    return av_semaphore2
  }
}

def write_json( String file_path , Map data_json ){
  def json = JsonOutput.toJson( data_json )
  json = JsonOutput.prettyPrint(json)
  writeFile(file: file_path, text : json)
}

def wait_block(){
  waitUntil{
    def fileContent = readFile("${host_path}/build/status.txt")
    if (fileContent.contains('OPEN')) {
        return false
    } else {
        return true
    }
  }
}

pipeline{
  agent {
      label 'ariel'
  }
  parameters{
      string(name : 'test_group', defaultValue : "dummy" )
      string(name : 'cmd_json_path', defaultValue : "./.test_file/test_cm.json" )
      string(name : 'host_job', defaultValue : '1.GLOBAL-SEMAPHORE')
      // string(name : 'host_path', defaultValue : '/var/lib/jenkins/workspace/TEST_SEM/2.HOST')
      string(name : 'project', defaultValue : 'None')
  }

  stages{
    stage("Set_command"){
      steps{
        script{
          cleanWs()
          checkout([
            $class: 'GitSCM'
          , branches: [[name: 'MGA-312']]
          , userRemoteConfigs: [[url: env.GIT_URL]]])

          def tmp_job_name = "${JOB_NAME.substring(JOB_NAME.lastIndexOf('/') + 1, JOB_NAME.length())}"
          semaphore_file_name = "${params.projcet}_${tmp_job_name}_${env.BUILD_NUMBER}"

          def buf_cmd_list = readJSON file: params.cmd_json_path
          tmp_command.addAll(buf_cmd_list)

          write_json( "${env.WORKSPACE}/cmd_list.json", [ 'cmd_list' : tmp_command ])
        }
      }
    }
    stage("Host_checking"){
      steps{
        script{
          def host_fullname
          waitUntil{
            name = params.host_job
            def items = new LinkedHashSet();
            def job = Hudson.instance.getJob(name)
            Jenkins.instance.getAllItems(AbstractItem.class).each{
              println it.fullName + " - " + it.class
              if( (it.fullName).contains(params.host_job) ){
                items.add(it.fullName);
                print("Fine global semaphore :: ${it.fullName}")
                Jenkins.instance.getItemByFullName(it.fullName).builds.each { build ->
                    if (build.building) {
                      host_fullname = it.fullName
                      print("Build ${host_fullname} -- ${build.building} is currently running")
                    }
                }
              }
            };
            if(items != null){
              print(job)
              return true
            }
            sleep(100)
            return false
          }
          host_path = sh(returnStdout: true, script: """
            #!/bin/zsh
            module load python/python/3.7.1
            python3.7 ${env.WORKSPACE}/libs/Find_host_path.py --host=${host_fullname} --workspace=${env.WORKSPACE} --job_name=${env.JOB_NAME}
          """).trim()
          print("Host path :: ${host_path}")
          sleep(10)
        }
      }
    }
    stage("Running"){
      steps{
        script{
          def tmp_cmd = [:]

          def ca = new AV_semaphore()

          print(" Command size :: ${tmp_command.size()}")

          tmp_cmd["0"] = {
            stage("checking_semaphore"){
              stage("register_host"){
                script{
                  write_json( "${host_path}/build/slave_add/${semaphore_file_name}", [ "${env.WORKSPACE}" : tmp_command.size() ])
                }
              }
              stage("update"){
                script{
                  waitUntil{
                    sleep(5)
                    if ( fileExists('semaphore_reg') ) {

                      def tmp_file = readJSON file: 'semaphore_reg'
                      def res = tmp_file[0]
                      sh("rm semaphore_reg")
                      ca.updatenumber(res)
                      print("Update available semaphore from host ${res}")
                      now_q_lengh+=res
                    }
                    if(ca.get_sem() >= tmp_command.size()){
                      return true
                    }
                    return false
                  }
                }
              }
            }
          }

          def num_buf = []
          (1..(tmp_command.size())).each{ i ->
            num_buf.add(i)
          }
          num_buf.each{ i2 ->
            tmp_cmd["${i2}"] = {
              stage("${tmp_command[i2-1]['name']}"){
                stage("wating_${tmp_command[i2-1]['name']}"){
                  script{
                    waitUntil{
                      if( ca.get_sem() >= i2){ return true }
                      return false
                    }
                    sleep(i2*5)
                  }
                }
                stage("Running_command_${tmp_command[i2-1]['name']}"){
                  script{
                    print("in running :: ${tmp_command[i2-1]['cmd']}")
                    sh(script : tmp_command[i2-1]['cmd'])
                  }
                }
                stage("Update_DB_${i2}"){
                  script{
                    wait_block()
                    print("Update DB data to Dashboard")
                    write_json( "${host_path}/build/slave_rm/${semaphore_file_name}_${i2}", ["${env.WORKSPACE}" : 1])
                    now_q_lengh--
                  }
                }
              }
            }
          }

          parallel tmp_cmd

        }
      }
    }
  }
  post{
    always{
      script{
        write_json( "${host_path}/build/slave_rm/${semaphore_file_name}_done", ["${env.WORKSPACE}" : now_q_lengh])
      }
    }
  }
}