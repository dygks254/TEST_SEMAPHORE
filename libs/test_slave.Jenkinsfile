import groovy.json.*
import java.io.File

tmp_command = []
semaphore_file_name = ""
host_path = ""
def now_q_lengh = 0
def simulation_result = [:]

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
      string(name : 'test_group', defaultValue : "backdoor0" )
      string(name : 'cmd_json_path', defaultValue : "./.test_file/test_cm.json" )
      string(name : 'host_job', defaultValue : '1.GLOBAL-SEMAPHORE')
      string(name : 'project', defaultValue : 'RHEA_EVT1')
      string(name : 'summary_execute', defaultValue : '/user/jenkins/LOGIC_CI/PROJECT/RHEA_EVT1/execute')
      string(name : 'commit', defaultValue : '')
  }

  stages{
    stage("Set_command"){
      steps{
        script{
          cleanWs()
          checkout([
            $class: 'GitSCM'
          , branches: [[name: 'master']]
          , userRemoteConfigs: [[url: env.GIT_URL]]])

          def tmp_job_name = "${JOB_NAME.substring(JOB_NAME.lastIndexOf('/') + 1, JOB_NAME.length())}"
          semaphore_file_name = "${params.project}_${tmp_job_name}_${env.BUILD_NUMBER}"

          def buf_cmd_list = readJSON file: params.cmd_json_path
          tmp_command.addAll(buf_cmd_list)

          write_json( "${env.WORKSPACE}/cmd_list.json", [ 'cmd_list' : tmp_command ])
        }
      }
    }
    stage("Host_checking"){
      steps{
        script{
          def host_fullname = ""
          waitUntil{
            name = params.host_job
            // def items = new LinkedHashSet();
            def job = Hudson.instance.getJob(name)
            Jenkins.instance.getAllItems(AbstractItem.class).each{
              // println it.fullName + " - " + it.class
              if( (it.fullName).contains(params.host_job) ){
                print("Find global semaphore :: ${it.fullName}")
                Jenkins.instance.getItemByFullName(it.fullName).builds.each { build ->
                    if (build.building) {
                      // items.add(it.fullName);
                      host_fullname = it.fullName
                      print("Build ${host_fullname} -- ${build.building} is currently running")
                    }
                }
              }
            };
            if( host_fullname != ""){
              print(job)
              return true
            }
            sleep(60)
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
    stage("Make_summary"){
      steps{
        script{
          def summary_test_groups_path = "${summary_execute}/${params.test_group}/result"
          sh(script:"""
            if [ ! -d ${summary_test_groups_path} ]; then
              mkdir -p ${summary_test_groups_path}
            fi
            """, returnStatus:true)
          def test_list = tmp_command.each{ each ->
            simulation_result["${summary_execute}/${params.test_group}/${each['name']}"] = "running"
          }
          // simulation_result = [ "used_tc" : test_list]
          write_json( "${summary_test_groups_path}/latest_used.json", simulation_result )
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
                def curl_sim_result = ""
                def res_c_status
                stage("wating_${tmp_command[i2-1]['name']}"){
                  script{
                    waitUntil{
                      if( ca.get_sem() >= i2){ return true }
                      return false
                    }
                    sleep(i2*100)
                    sh("""
                        curl -X POST \
                            -H "Content-Type: application/json" \
                            -d '{
                              "project" : "${params.project}",
                              "test_list" : "${params.test_group}",
                              "name" : "${tmp_command[i2-1]['name']}",
                              "Result" : "RUNNING",
                              "SimPath" : "${tmp_command[i2-1]['sim_path']}",
                              "Command" : "${tmp_command[i2-1]['slurm_cmd']}",
                              "Commit" : "${params.commit}"
                            }' http://portal:8002/jenkins_simulation/
                    """)
                  }
                }
                stage("Running_command_${tmp_command[i2-1]['name']}"){
                  script{
                    print("in running :: ${tmp_command[i2-1]['cmd']}")
                    def res = sh(script : tmp_command[i2-1]['cmd'], returnStatus:true)
                    if(res != 0){
                      print("Slurm failed :: Running_command_${tmp_command[i2-1]['name']} ")
                      curl_sim_result = "SLRUM_FAILED"
                    }
                  }
                }
                stage("Update_DB_${i2}"){
                  script{
                    wait_block()

                    res_execute_status = sh(script:"readlink -f ${tmp_command[i2-1]['sim_path']}/${tmp_command[i2-1]['name']}*", returnStatus:true)
                    res_c_status = sh(script:"readlink -f ${tmp_command[i2-1]['c_comp_path']}/${tmp_command[i2-1]['name']}/debug/${tmp_command[i2-1]['name']}.hex", returnStatus:true)
                    def res_status = sh(script:"readlink -f ${tmp_command[i2-1]['sim_path']}/${tmp_command[i2-1]['name']}*/status.log", returnStatus:true)

                    def last_sim_path = "${tmp_command[i2-1]['sim_summary_path']}/${params.test_group}/${tmp_command[i2-1]['name']}"

                    if( ((curl_sim_result == "SLRUM_FAILED") || (res_execute_status != 0)) && ( res_c_status == 0) ){
                      print("Slurm failed")
                    }else if( res_c_status != 0){
                      print("Directory not exit :: ${tmp_command[i2-1]['sim_path']}/${tmp_command[i2-1]['name']}*")
                      curl_sim_result = "C_FAILED"
                      last_sim_path = "${tmp_command[i2-1]['c_comp_path']}/${tmp_command[i2-1]['name']}"
                    }else if( res_status != 0){
                      print("File not exit :: ${tmp_command[i2-1]['sim_path']}/${tmp_command[i2-1]['name']}*/status.log")
                      curl_sim_result = "FAILED"
                    }else{
                      print("File exit :: ${tmp_command[i2-1]['sim_path']}/${tmp_command[i2-1]['name']}*/status.log")
                      def status_path = sh(script:"cat ${tmp_command[i2-1]['sim_path']}/${tmp_command[i2-1]['name']}*/status.log", returnStdout: true)
                      // def sim_result = readFile(status_path)
                      if(status_path.contains("PASS")){
                        curl_sim_result = "PASSED"
                      }else if( curl_sim_result != "SLRUM_FAILED" ){
                        curl_sim_result = "FAILED"
                      }
                    }

                    print("Update DB data to Dashboard")
                    write_json( "${host_path}/build/slave_rm/${semaphore_file_name}_${i2}", ["${env.WORKSPACE}" : 1])
                    now_q_lengh--

                    sh("""
                        curl -X POST \
                            -H "Content-Type: application/json" \
                            -d '{
                              "project" : "${params.project}",
                              "test_list" : "${params.test_group}",
                              "name" : "${tmp_command[i2-1]['name']}",
                              "Result" : "${curl_sim_result}",
                              "SimPath" : "${last_sim_path}"
                            }' http://portal:8002/jenkins_simulation/
                    """)
                  }
                }
                stage("Update_COV_${i2}"){
                  if(res_c_status == 0){
                    print("Update COVERAGE data to Dashboard")
                    def res_excute_path = sh(script:""" find ${tmp_command[i2-1]['sim_path']} -name "${tmp_command[i2-1]['name']}*" -type d -regex ".+\\.[0-9]+" -printf '%T@\t%p\n' | perl -ane '@m=@F if (\$F[0]>\$m[0]); END{print \$m[1];}' """,returnStdout:true)
                    sh(script:"nice -n 10 rsync -a --progress --delete ${res_excute_path}/  ${params.summary_execute}/${params.test_group}/${tmp_command[i2-1]['name']}")
                  }else{
                    print("Can't Update COVERAGE data to Dashboard")
                  }
                  simulation_result["${summary_execute}/${params.test_group}/${tmp_command[i2-1]['name']}"] = curl_sim_result
                  write_json( "${summary_execute}/${params.test_group}/result/latest_used.json", simulation_result )
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
