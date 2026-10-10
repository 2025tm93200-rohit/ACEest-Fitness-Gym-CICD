pipeline {
  agent any
  environment {
    IMAGE_NAME = "aceest-fitness-gym"
    IMAGE_TAG = "${BUILD_NUMBER}"
  }
  stages {
    stage("Checkout") {
      steps { checkout scm }
    }
    stage("Build") {
      steps { sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ." }
    }
    stage("Syntax Check") {
      steps { sh "docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} python -m py_compile app.py" }
    }
    stage("Automated Tests") {
      steps { sh "docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} pytest -q" }
    }
    stage("Quality Gate") {
      steps { sh "docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} flake8 app.py tests" }
    }
  }
  post {
    always { sh "docker image rm ${IMAGE_NAME}:${IMAGE_TAG} || true" }
  }
}