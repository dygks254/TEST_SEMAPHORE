pipeline{
  agent {
      label "sun"
  }
  parameters {
    string(name : 'project', defaultValue: 'RHEA_EVT1', description: 'Project name')
    string(name : 'url', description: 'Confluence URL')
  }
  stages{
    stage("Set"){
      steps{
        script{
          cleanWs()
          checkout([
            $class: 'GitSCM'
            ,branches: [[name: 'master']]
            ,userRemoteConfigs: [[url: "git@portal:infrastructure/ld_dashboard_email.git" ]]])

          top_repo = "ld_dashboard_email"
          set_output_dir = "${env.WORKSPACE}/build"
          set_templates_dir = "${env.WORKSPACE}/templates"
        }
      }
    }
    stage('Run'){
      steps{
        script{
          sh("""
            module load python/python/3.7.1
            python3.7 ${env.WORKSPACE}/main.py --project ${env.project} --url ${env.url} --output_dir ${set_output_dir} --templates_dir ${set_templates_dir}
          """)
        }
      }
    }
  }
}
