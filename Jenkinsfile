pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = "ap-south-1"
    }

    stages {

        stage('Validate') {
            steps {
                sh '''
                sh 'ls -l'
                python3 -m py_compile services/addToCart/lambda_function.py
                python3 -m py_compile services/getCart/lambda_function.py
                python3 -m py_compile services/checkoutCart/lambda_function.py
                python3 -m py_compile services/getOrders/lambda_function.py
                '''
            }
        }

        stage('Package') {
            steps {
                sh '''
                cd services/addToCart && zip -r function.zip .
                cd ../getCart && zip -r function.zip .
                cd ../checkoutCart && zip -r function.zip .
                cd ../getOrders && zip -r function.zip .
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                aws lambda update-function-code \
                --function-name addToCart \
                --zip-file fileb://services/addToCart/function.zip

                aws lambda update-function-code \
                --function-name getCart \
                --zip-file fileb://services/getCart/function.zip

                aws lambda update-function-code \
                --function-name checkoutCart \
                --zip-file fileb://services/checkoutCart/function.zip

                aws lambda update-function-code \
                --function-name getOrders \
                --zip-file fileb://services/getOrders/function.zip
                '''
            }
        }

    }
}
