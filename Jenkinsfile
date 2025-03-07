pipeline {
    agent any

    environment {
        IMAGE_NAME = "shamailkhan/crime-prediction-la"
        IMAGE_TAG = "latest"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    bat "docker build -t %IMAGE_NAME%:%IMAGE_TAG% ."
                }
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    bat "echo %DOCKER_PASS% | docker login -u %DOCKER_USER% --password-stdin"
                }
            }
        }

        stage('Push Image to Docker Hub') {
            steps {
                script {
                    bat "docker push %IMAGE_NAME%:%IMAGE_TAG%"
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    bat "docker rmi %IMAGE_NAME%:%IMAGE_TAG%"
                }
            }
        }
    }

    post {
        success {
            echo " Build and Deployment Successful!"
            
            emailext subject: " Deployment Successful: Crime-Prediction in LA",
                     body: """
                     Hello Admin,

                     The deployment of crime prediction in la  has been successfully completed.

                     Regards,  
                     Jenkins
                     """,
                     to: "emanfurrukh09@gmail.com",
                     from: "shamailkhan757@gmail.com",
                     replyTo: "shamailkhan757@gmail.com"
        }
        failure {
            echo " Build Failed. Check logs for details."
        }
    }
}