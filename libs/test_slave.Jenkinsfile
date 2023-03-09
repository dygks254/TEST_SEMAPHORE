import groovy.json.*
import java.io.File

tmp_command = []

class AV_semaphore{
  int av_semaphore2 = 0
  void updatenumber(int number){
    av_semaphore2 += number
  }
  int get_sem(){
    return av_semaphore2
  }
}

pipeline{

  agent any

  parameters{
      string(name : 'cmd_json_path', defaultValue : '/home/yohan/PROJECT/2.JENKINS/STAGE/test_data_dir/tmp_data.json' )
      string(name : 'host_path', defaultValue : '/var/lib/jenkins/workspace/TEST_SEM/1.HOST_SEMAPHORE')
  }

  stages{
    stage("Set_command"){
      steps{
        script{
          cleanWs()

          def buf_cmd_list = readJSON file: params.cmd_json_path
          tmp_command.addAll(buf_cmd_list)

          def json = JsonOutput.toJson( [ 'cmd_list' :[tmp_command]] )
          json = JsonOutput.prettyPrint(json)
          writeFile(file: "${env.WORKSPACE}/cmd_list.json", text : json)

          writeFile(file: 'test1', text: "0", encoding: "UTF-8")
        }
      }
    }
    stage("Running"){
      steps{
        script{
          def tmp_cmd = [:]

          def ca = new AV_semaphore()

          print("number :: ${tmp_command.size()}")
          ca.updatenumber(number = 1)
          print("number :: ${tmp_command.size()}")

          tmp_cmd["0"] = {
            stage("up"){
              script{
                waitUntil{
                  sleep(5)
                  if ( fileExists('test1') ) {
                    def tmp_file = readFile('test1')
                    sh("rm test1")
                    def res = Integer.parseInt(tmp_file.trim())
                    ca.updatenumber(number = res)
                  }
                  if(ca.get_sem() >= tmp_command.size()){
                    return true
                  }
                  return false
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
              stage("${i2}"){
                stage("wating_${i2}"){
                  script{
                    waitUntil{
                      print( "${ca.get_sem()}  ::  ${i2}" )
                      if( ca.get_sem() >= i2){
                        return true
                      }
                      return false
                      return true
                    }
                    print("in para")
                  }
                }
                stage("Running_command_${i2}"){
                  script{
                    print("in running :: ${tmp_command[i2-1]}")
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
}