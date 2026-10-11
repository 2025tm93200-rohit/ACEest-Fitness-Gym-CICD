pipeline {
  agent any

  environment {
    IMAGE_NAME = "aceest-fitness-gym"
    IMAGE_TAG = "${BUILD_NUMBER}"
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
        bat "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
      }
    }

    stage("Syntax Check") {
      steps {
        bat "docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} python -m py_compile app.py"
      }
    }

    stage("Automated Tests") {
      steps {
        bat "docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} pytest -q"
      }
    }

    stage("Quality Gate") {
      steps {
        bat "docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} flake8 app.py tests"
      }
    }
  }

  post {
    always {
      bat "docker image rm ${IMAGE_NAME}:${IMAGE_TAG} || exit /b 0"
    }
  }
}