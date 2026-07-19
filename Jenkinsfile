pipeline {
agent any

environment {
    AWS_REGION = "ap-south-1"
    AWS_ACCOUNT_ID = "886682668143"
    ECR_REPO = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/cart-service"
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
stage('Render ECS Task Definition') {
    steps {
        sh """
        sed \
          -e "s|IMAGE_URI|$ECR_REPO:$IMAGE_TAG|g" \
          -e "s|ACCOUNT_ID|$AWS_ACCOUNT_ID|g" \
          -e "s|AWS_REGION_PLACEHOLDER|$AWS_REGION|g" \
          infra/ecs-task-def-template.json > ecs-task-def.json
        """
        sh "cat ecs-task-def.json"
    }
}
   stage('Deploy to ECS') {
    steps {
        script {
            def taskDefArn = sh(
                script: """
                aws ecs register-task-definition \
                  --cli-input-json file://ecs-task-def.json \
                  --query 'taskDefinition.taskDefinitionArn' \
                  --output text
                """,
                returnStdout: true
            ).trim()

            sh """
            aws ecs update-service \
              --cluster $CLUSTER \
              --service $SERVICE \
              --task-definition ${taskDefArn} \
              --region $AWS_REGION

            aws ecs wait services-stable \
              --cluster $CLUSTER \
              --services $SERVICE \
              --region $AWS_REGION
            """
        }
    }
}
   
    }
}
