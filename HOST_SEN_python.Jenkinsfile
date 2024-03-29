import groovy.json.*

configuration = [
  'agent' : "ariel"
]

pipeline {
  agent {
      label configuration['agent']
  }
  parameters{
      string(name: 'semaphore', defaultValue: '10')
  }
  stages {
    stage ('Initialize') {
      steps {
        cleanWs()

        checkout([
            $class: 'GitSCM'
          , branches: [[name: 'master']]
          , userRemoteConfigs: [[url: env.GIT_URL]]])

        script{
          def json = JsonOutput.toJson([
             'build_path' : "${env.WORKSPACE}/build"
            ,'q_file' : "${env.WORKSPACE}/build/semaphore_q.json"
            ,'total_q' : (params.semaphore).toInteger()
            ,'r_file' : "${env.WORKSPACE}/build/running.txt"
            ,'add_list' : "${env.WORKSPACE}/build/slave_add"
            ,'rm_list' : "${env.WORKSPACE}/build/slave_rm"
            ,'status'  : "${env.WORKSPACE}/build/status.txt"
          ])
          configuration_file = "${env.WORKSPACE}/python_source.json"
          print(configuration_file)
          json = JsonOutput.prettyPrint(json)
          writeFile(file: configuration_file, text : json)
        }
      }
    }
    stage('Start_HOST'){
      steps{
        script{
          sh"""
            #!/bin/zsh
            module purge
            module load python/python/3.7.1
            python3.7 libs/Host_semaphore.py --source ${configuration_file} > test_log.log
          """
        }
      }
    }
  }
  post {
        always{
          script{
              print("${env.WORKSPACE}/build/running.txt")
              writeFile(file : "${env.WORKSPACE}/build/running.txt", text : 'FALSE')
          }
        }
  }

}
