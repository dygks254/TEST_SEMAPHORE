import groovy.json.*

configuration = [:]

String [] checking_slave( file_path ){
  def fileContent = readFile file_path
  def tmp_list = fileContent.split(', ')
  tmp_list = tmp_list.findAll { it != tmp_list.first() }
  def newArray = tmp_list.findAll { it.replace("\n","") }
  print(newArray)
  return newArray
}

def write_json( String file_path , Map data_json ){
  def json = JsonOutput.toJson( data_json )
  json = JsonOutput.prettyPrint(json)
  writeFile(file: configuration['q_file'], text : json)
}

def update_json( test_path , String update_type = "add" ){
  print("in update json")
  test_path.each{ now_path ->
    if( update_type == "add"){
      // configuration['test'].add(now_path)
      // configuration['test_list'] = configuration['test_list'].addAll(test_path)
      print(configuration['test_list'].getClass())
      print(test_path.getClass())
      print("ssssssssss")
      configuration['test_list'] += test_path
      print("sed -i '/${now_path.replaceAll("\n", "")}/d' ${configuration['add_list']}")
      sh("sed -i '/${now_path.replaceAll("\n", "")}/d' ${configuration['add_list']}")
    }else{
      configuration['test_list'].remove(configuration['test_list'].indexOf(now_path))
      // sh("sed -i '/${now_path.replace('/','\/')}/d' ${configuration['add_list]'}")
    }
  }
  print(configuration['test_list'])
  write_json( file_path = configuration['q_file'], data_json = [ 'total_q' : configuration['total_q'], 'test' : configuration['test_list'] ] )
}

pipeline{
  agent any

  parameters{
      string(name: 'semaphore', defaultValue: '10')
  }
  stages{
    stage("Setting"){
      steps{
        script{
          cleanWs()

          configuration['q_file'] = "${env.WORKSPACE}/semaphore_q.json"
          configuration['total_q'] = (params.semaphore).toInteger()
          write_json( file_path = configuration['q_file'], data_json = [ 'total_q' : configuration['total_q'] , 'test' : []] )

          configuration['test_list'] = []

          configuration['r_file'] = "${env.WORKSPACE}/running.txt"
          writeFile(file: configuration['r_file'], text: "running", encoding: "UTF-8")

          configuration['add_list'] = "${env.WORKSPACE}/slave_add.txt"
          configuration['rm_list'] = "${env.WORKSPACE}/slave_rm.txt"
          writeFile(file: configuration['add_list'], text: "", encoding: "UTF-8")
          writeFile(file: configuration['rm_list'],  text: "", encoding: "UTF-8")
        }
      }
    }
    stage("test"){
      steps{
        // def file = new File('/home/yohan/PROJECT/2.JENKINS/STAGE/test_folder/file.txt')
        script{
          while( readFile(file: configuration['r_file'] ) == 'running' ){
            waitUntil{
              sleep(3)
              tmp_list = checking_slave(configuration['add_list'])
              print(" test list :: ${tmp_list}   :: ${tmp_list.size()}")
              if( tmp_list.size() > 0 ){
                update_json( test_path = tmp_list)
              }

              configuration['q_status'] = readJSON file: configuration['q_file']
              if ( configuration['q_status']['total_q'] != 0 ){
                return true
              }
              return false
            }
          }
        }
      }
    }
  }
}