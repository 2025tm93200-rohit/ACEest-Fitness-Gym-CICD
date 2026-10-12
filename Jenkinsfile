pipeline {
  agent any

  environment {
    IMAGE_NAME = "aceest-fitness-gym"
    IMAGE_TAG = "${BUILD_NUMBER}"
    SONAR_HOST_URL = "http://sonarqube:9000"
    SONAR_PROJECT_KEY = "aceest-fitness-gym"
  }

  triggers {
    pollSCM('* * * * *')
  }

  stages {
    stage("Checkout") {
      steps {
        checkout scm
      }
    }

    stage("Build") {
      steps {
        bat "docker buildx build --load -t ${IMAGE_NAME}:${IMAGE_TAG} ."
      }
    }

    stage("Syntax Check") {
      steps {
        bat "docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} python -m py_compile app.py"
      }
    }

    stage("Automated Tests") {
      steps {
        bat "docker run --rm -e PYTHONPATH=/app ${IMAGE_NAME}:${IMAGE_TAG} pytest -q"
      }
    }

    stage("Quality Gate") {
      steps {
        bat "docker run --rm -e PYTHONPATH=/app ${IMAGE_NAME}:${IMAGE_TAG} flake8 app.py tests"
      }
    }

    stage("SonarQube Analysis") {
      steps {
        withCredentials([string(credentialsId: 'sonarqube-token', variable: 'SONAR_TOKEN')]) {
          bat """
          docker run --rm ^
            -e SONAR_HOST_URL=%SONAR_HOST_URL% ^
            -e SONAR_TOKEN=%SONAR_TOKEN% ^
            -v "%cd%":/usr/src ^
            sonarsource/sonar-scanner-cli:latest
          """
        }
      }
    }
  }

  post {
    always {
      bat "docker image rm ${IMAGE_NAME}:${IMAGE_TAG} || exit /b 0"
    }
  }
}