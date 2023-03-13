
// @Grab(group='org.codehaus.groovy.modules.http-builder', module='http-builder', version='0.7')
// import groovyx.net.http.HTTPBuilder


NOW_WORKSPACE = ""

jenkins_url = "http://localhost:8080"

pipeline{
  agent any
  stages{
    stage('first'){
      steps{
        script{

          def temp_string = sh(script: 'pwd', returnStdout: true).trim()
          print(temp_string)
          cleanWs()
          checkout([
              $class: 'GitSCM'
            , branches: [[name: 'create_job']]
            , userRemoteConfigs: [[url: env.GIT_URL]]])

          def split_name = ("${env.JOB_NAME}").split('/') as List
          split_name.remove(split_name[-1])
          NOW_WORKSPACE = split_name
          print(NOW_WORKSPACE)
        }
      }
    }
    // stage('dummy'){
    //   def jenkinsUrl="https://localhost:8080/";
    //   //def jenkinsUrl="http://192.168.0.10:1010";
    //   def auth="admin:semi12!@".bytes.encodeBase64().toString()
    //   def httpBuilder=new HTTPBuilder(jenkinsUrl);

    //   /**
    //   * GET CRUMB
    //   */
    //   def crumbResult=httpBuilder.request(Method.GET, ContentType.JSON){
    //       headers."authorization" = "Basic ${auth}"
    //       uri.path = "/crumbIssuer/api/json";

    //       response.success = { resp, body ->
    //           println "Jenkins Called Successfully";
    //           println "resp status:${resp.status}, json:${body}"
    //           return body;
    //       }
    //       response.failure={resp, body ->
    //           log.info("${resp.status} - ${body}")
    //           def msg="failed ";
    //           throw new Exception(msg);
    //       }
    //   }
    //   def crumb=crumbResult["crumb"]
    //   log.info "crumb:${crumb}";

    //   def postBody= [SYSTEM: system,
    //                 ISSUE_IDS: issueId,
    //                 TRUNK_SVNURL: trunkSvnUrl,
    //                 JOB_PATH: jobPath,
    //                 PHASE: phase,
    //                 LOW_VERSION_CHECK: lowVersionCheck,
    //                 COPY_TEMP: copyTemp,
    //                 EXTENTIONS: extensions,
    //                   ];
    //   httpBuilder.request(Method.POST, ContentType.URLENC){
    //       uri.path="/job/${jenkinsJobName}/buildWithParameters";
    //       headers."authorization"="Basic ${auth}"
    //       headers."Jenkins-Crumb"=crumb;
    //       body=paramJson;

    //       response.success={resp, json ->
    //           log.info  "Jenkins Called Successfully";
    //           log.info "resp status:${resp.status}, json:${json}"
    //       }
    //       response.failure={resp, body ->
    //           log.info("${resp.status} - ${body}")
    //           def msg="failed ";
    //           throw new Exception(msg);
    //       }
    //   }
    // }
    stage('seconde'){
      steps{
        script{

          def jobName = ["test_slave01","test_slave02","test_slave03"]

          def tmp_job_folder = ""
          NOW_WORKSPACE.each{ each ->
            tmp_job_folder += "/job/${each}"
          }

          print(tmp_job_folder)

          withCredentials([string(credentialsId: 'portal_jenkins', variable: 'API_TOKEN')]) {


            // command_get_crumb = """
            //   curl -s '${jenkins_url}/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)' \
            //     -u ${API_TOKEN}
            // """
            // final String response_crumb = sh(script: command_get_crumb , returnStdout: true).trim()
            // print(response_crumb)

            command_checking_folder = """
              curl -X GET \
                ${jenkins_url}${tmp_job_folder}/job/TEST_LIST/config.xml \
                -u ${API_TOKEN}
            """
            final String response_checking_folder = sh(script: command_checking_folder , returnStdout: true).trim()
            print(response_checking_folder)

            if( response_checking_folder.contains("Error 40") ){
              print("Please make folder ${tmp_job_folder}/job/TEST_LIST")

              command_create_folder = """
                curl -X POST \
                  '${jenkins_url}${tmp_job_folder}/createItem?name=TEST_LIST&mode=com.cloudbees.hudson.plugins.folder.Folder&from=&json=%7B%22name%22%3A%22FolderName%22%2C%22mode%22%3A%22com.cloudbees.hudson.plugins.folder.Folder%22%2C%22from%22%3A%22%22%2C%22Submit%22%3A%22OK%22%7D&Submit=OK' \
                  --user ${API_TOKEN} \
                  -H "Content-Type:application/x-www-form-urlencoded"
              """
              final String response_create_folder = sh(script: command_create_folder , returnStdout: true).trim()
              print(response_create_folder)
              if( response_create_folder.contains("Error 40")){
                error("Failed create folder ${tmp_job_folder}/job/TEST_LIST")
              }

            }

            def items = new LinkedHashSet();
            jobName.each{ each ->
              if( !Hudson.instance.getJob(each)){
                print("Please make job ${each}")

                command_create_jobs = """
                  curl -s -X POST \
                    '${jenkins_url}${tmp_job_folder}/job/TEST_LIST/createItem?name=${each}' \
                    -u ${API_TOKEN} \
                    --data-binary @libs/slave_config.xml \
                    -H "Content-Type:text/xml"
                """
                final String response_create_job = sh(script: command_create_jobs , returnStdout: true).trim()
                print(response_create_job)
                if( response_create_job.contains("Error 40")){
                  error("Failed create job ${tmp_job_folder}/job/TEST_LIST  -->  ${each}")
                }
              }
            }

          }



          // // Create new job in folder
          // def folderPath = NOW_WORKSPACE
          // def folder = jenkins.model.Jenkins.instance.getItemByFullName(folderPath)
          // if (!folder) {
          //   jenkins.model.Jenkins.instance.createProject(com.cloudbees.hudson.plugins.folder.Folder, folderPath)
          // }
          // else{
          //   print("Already exist ${folderPath}")
          // }



        }
      }
    }
  }
}