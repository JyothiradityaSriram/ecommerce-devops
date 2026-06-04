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
            dir('services/cart-service') {
                sh """
                docker build -t $ECR_REPO:$IMAGE_TAG .
                """
            }
        }
    }

    stage('Login to ECR') {
        steps {
            sh """
            aws ecr get-login-password --region $AWS_REGION \
            | docker login --username AWS --password-stdin $ECR_REPO
            """
        }
    }

    stage('Push Docker Image') {
        steps {
            sh """
            docker push $ECR_REPO:$IMAGE_TAG
            """
        }
    }

   stage('Deploy to ECS') {
steps {
sh """
TASK_DEF_ARN=$(aws ecs register-task-definition  --cli-input-json file://ecs-task-def.json --query 'taskDefinition.taskDefinitionArn' --output text)


    aws ecs update-service \
      --cluster $CLUSTER \
      --service $SERVICE \
      --task-definition $TASK_DEF_ARN \
      --region $AWS_REGION

    aws ecs wait services-stable \
      --cluster $CLUSTER \
      --services $SERVICE \
      --region $AWS_REGION
    """
}
}

