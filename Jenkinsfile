pipeline {
agent any

```
environment {
    AWS_DEFAULT_REGION = "ap-south-1"
}

stages {

    stage('Validate') {
        steps {
            sh '''
            set -e
            python3 -m py_compile services/addToCart/lambda_function.py
            python3 -m py_compile services/getCart/lambda_function.py
            python3 -m py_compile services/checkoutCart/lambda_function.py
            python3 -m py_compile services/getOrders/lambda_function.py
            python3 -m py_compile services/getProduct/lambda_function.py
            python3 -m py_compile services/getProducts/lambda_function.py
            '''
        }
    }

    stage('Package') {
        steps {
            sh '''
            set -e

            # Clean old zips
            rm -f services/*/function.zip

            # Controlled packaging (ONLY required files)
            cd services/addToCart && zip function.zip lambda_function.py && cd ../../
            cd services/getCart && zip function.zip lambda_function.py && cd ../../
            cd services/checkoutCart && zip function.zip lambda_function.py && cd ../../
            cd services/getOrders && zip function.zip lambda_function.py && cd ../../
            cd services/getProduct && zip function.zip lambda_function.py && cd ../../
            cd services/getProducts && zip function.zip lambda_function.py && cd ../../
            '''
        }
    }

    stage('Deploy') {
        steps {
            sh '''
            set -e

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

            aws lambda update-function-code \
            --function-name getProduct \
            --zip-file fileb://services/getProduct/function.zip

            aws lambda update-function-code \
            --function-name getProducts \
            --zip-file fileb://services/getProducts/function.zip
            '''
        }
    }

}
```

}
