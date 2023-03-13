
import jenkins.model.*
import hudson.model.*


NOW_WORKSPACE = ""


pipeline{
  agent any
  stages{
    stage('first'){
      steps{
        script{
          def split_name = ("${env.JOB_NAME}").split('/') as List
          split_name.remove(split_name[-1])
          NOW_WORKSPACE = split_name.join("/")
          print(NOW_WORKSPACE)
        }
      }
    }
    stage('seconde'){
      steps{
        script{

          // def jobName = "test_jobs1"

          // // Create new job in folder
          // def folderPath = NOW_WORKSPACE
          // def folder = jenkins.model.Jenkins.instance.getItemByFullName(folderPath)
          // if (!folder) {
          //   jenkins.model.Jenkins.instance.createProject(com.cloudbees.hudson.plugins.folder.Folder, folderPath)
          // }
          // else{
          //   print("Already exist ${folderPath}")
          // }

          // def jobs = jenkins.model.Jenkins.instance.getItemByFullName("${folderPath}/${jobName}")
          // if(!jobs){
          //   print("Please create jobs")
          //   folder.createProject(hudson.model.FreeStyleProject, jobName)
          // }

          // def config = """
          //   <project>
          //       <description>My updated job description</description>
          //       <builders>
          //           <hudson.tasks.Shell>
          //               <command>echo 'Hello, world!'</command>
          //           </hudson.tasks.Shell>
          //       </builders>
          //   </project>
          // """
          // print(config.getClass())
          // def job = Jenkins.instance.getItemByFullName("${folderPath}/${jobName}")
          // job.updateByXml(config)
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
          // def job = Jenkins.instance.getItemByFullName("${folderPath}/${jobName}")
          // print("aaaaa")
          // def xmlConfig = job.configFile.xml
          // xmlConfig.replace("Old description", "New description")
          // print(xmlConfig )
          // job.updateByXmlString(xmlConfig.toString())

          // print("Already exist ${folderPath}/${jobName}")

          // def jobName = "my-pipeline-job"
          // def provider = configFileProvider([configFile(fileId: 'job-config', targetLocation: 'job-config.xml', variable: 'JOB_CONFIG')])
          // def xmlConfig = readFile(provider.variable)
          // print(xmlConfig)
          // xmlConfig.replace("Old description", "New description")
          // writeFile(file: provider.targetLocation, text: xmlConfig)
          // provider.provide()


          // Define a function to create a pipeline job




          def jobName = 'my-dsl-job'
          def jobScript = '''
          pipeline {
              agent any
              stages {
                  stage('Build') {
                      steps {
                          sh 'make'
                      }
                  }
                  stage('Test') {
                      steps {
                          sh 'make test'
                      }
                  }
                  stage('Deploy') {
                      steps {
                          sh 'make deploy'
                      }
                  }
              }
          }
          '''

          // Get the Jenkins instance
          def jenkins = Jenkins.getInstance()

          // Create a new job
          def job = jenkins.createProject(FreeStyleProject, jobName)

          // Add the DSL script as a string parameter
          job.addProperty(new ParametersDefinitionProperty(
              new StringParameterDefinition('SCRIPT', jobScript)
          ))

          // Set the build steps to execute the DSL script
          job.getBuildersList().add(new hudson.tasks.Shell("echo '${jobScript}' | groovy ="))

          // Save the job configuration
          job.save()

        }
      }
    }
  }
}