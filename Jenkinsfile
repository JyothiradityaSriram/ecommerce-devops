pipeline {
    agent any

    environment {
        AWS_REGION = "ap-south-1"
        ECR_REPO = "542175649814.dkr.ecr.ap-south-1.amazonaws.com/cart-service"
        CLUSTER = "cart-cluster"
        SERVICE = "cart-service"
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t cart-service:$IMAGE_TAG ."
                }
            }
        }

        stage('Login to ECR') {
            steps {
                script {
                    sh """
                    aws ecr get-login-password --region $AWS_REGION \
                    | docker login --username AWS --password-stdin $ECR_REPO
                    """
                }
            }
        }

        stage('Tag & Push Image') {
            steps {
                script {
                    sh """
                    docker tag cart-service:$IMAGE_TAG $ECR_REPO:$IMAGE_TAG
                    docker push $ECR_REPO:$IMAGE_TAG
                    """
                }
            }
        }

        stage('Deploy to ECS') {
            steps {
                script {
                    sh """
                    aws ecs update-service \
                      --cluster $CLUSTER \
                      --service $SERVICE \
                      --force-new-deployment \
                      --region $AWS_REGION
                    """
                }
            }
        }
    }
}
