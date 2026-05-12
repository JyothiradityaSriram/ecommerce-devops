# Serverless E-Commerce Backend on AWS

A fully serverless e-commerce backend built using AWS Lambda, API Gateway, DynamoDB, Cognito, and Jenkins CI/CD.

This project demonstrates:
- Serverless microservices architecture
- JWT authentication using AWS Cognito
- REST API development using Python + Boto3
- DynamoDB data modeling
- CI/CD automation using Jenkins
- Cloud-native backend deployment on AWS

---

# Architecture Overview

```text
Frontend
   |
   v
API Gateway
   |
   v
AWS Lambda Functions
   |
   +---- Products Table
   +---- Cart Table
   +---- Orders Table
   +---- OrderItems Table
   |
   v
DynamoDB
```

---

# Authentication Flow

```text
User Login
   |
   v
AWS Cognito
   |
   v
JWT Token
   |
   v
API Gateway Authorizer
   |
   v
Lambda Functions
```

---

# Features

- User authentication using AWS Cognito
- Add products to cart
- View cart with total price calculation
- Checkout functionality
- View order history
- REST APIs with API Gateway
- DynamoDB integration
- CI/CD pipeline using Jenkins
- Structured logging using CloudWatch
- CORS handling
- Error handling

---

# Tech Stack

## AWS Services
- AWS Lambda
- API Gateway
- DynamoDB
- Cognito
- CloudWatch Logs

## Backend
- Python 3
- Boto3

## DevOps
- Jenkins
- GitHub

---

# Repository Structure

```bash
ecommerce-devops/
│
├── infra/
│
├── services/
│   ├── addToCart/
│   │   └── lambda_function.py
│   │
│   ├── checkoutCart/
│   │   └── lambda_function.py
│   │
│   ├── getCart/
│   │   └── lambda_function.py
│   │
│   ├── getOrders/
│   │   └── lambda_function.py
│   │
│   ├── getProduct/
│   │   └── lambda_function.py
│   │
│   └── getProducts/
│       └── lambda_function.py
│
├── Jenkinsfile
├── .gitignore
└── README.md
```

---

# Microservices

| Service | Description |
|---|---|
| addToCart | Adds products into cart |
| getCart | Returns cart items with total |
| checkoutCart | Creates order from cart |
| getOrders | Returns user order history |
| getProduct | Returns single product |
| getProducts | Returns all products |

---

# DynamoDB Tables

## Products

| Attribute | Type |
|---|---|
| id | Partition Key |
| name | String |
| price | Number |
| image | String |
| description | String |

---

## cart

| Attribute | Type |
|---|---|
| userId | Partition Key |
| cartId | Sort Key |
| productId | String |
| quantity | Number |
| createdAt | String |

---

## Orders

| Attribute | Type |
|---|---|
| orderId | Partition Key |
| userId | Global Secondary Index |
| total | Number |
| createdAt | String |

---

## OrderItems

| Attribute | Type |
|---|---|
| orderId | Partition Key |
| productId | Sort Key |
| quantity | Number |
| price | Number |

---

# API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /products | Get all products |
| GET | /product?id=1 | Get single product |
| POST | /cart | Add product to cart |
| GET | /cart | Get user cart |
| POST | /checkout | Checkout cart |
| GET | /orders | Get order history |

---

# Example Request

## Add To Cart

### Request

```json
{
  "productId": "1",
  "quantity": 2
}
```

### Response

```json
{
  "message": "Item added to cart"
}
```

---

# Example Cart Response

```json
{
  "items": [
    {
      "productId": "1",
      "name": "Laptop",
      "price": 50000,
      "quantity": 2,
      "subtotal": 100000
    }
  ],
  "cartTotal": 100000
}
```

---

# JWT Authentication

This project uses AWS Cognito JWT authentication.

Each Lambda extracts user identity using:

```python
event["requestContext"]["authorizer"]["jwt"]["claims"]["sub"]
```

This ensures:
- User-level authorization
- Secure cart access
- Secure order history access

---

# CI/CD Pipeline

Jenkins pipeline automates:
- Python syntax validation
- Lambda packaging
- ZIP artifact generation
- Lambda deployment

---

# Jenkins Pipeline Stages

```text
Validate
   ↓
Package
   ↓
Deploy
```

---

# Example Deployment Command

```bash
aws lambda update-function-code \
--function-name getCart \
--zip-file fileb://services/getCart/function.zip
```

---

# Logging

CloudWatch logging enabled using:

```python
logger = logging.getLogger()
logger.setLevel(logging.INFO)
```

Benefits:
- Debugging
- Request tracing
- Error monitoring
- Operational visibility

---

# Security Features

Implemented:
- JWT Authentication
- User-level authorization
- CORS handling
- Error handling
- DynamoDB access isolation

---

# Local Development

## Install Dependencies

```bash
pip install boto3
```

---

## Validate Python Files

```bash
python3 -m py_compile services/getCart/lambda_function.py
```

---

# Deployment Requirements

- AWS Account
- Lambda Functions
- API Gateway HTTP API
- DynamoDB Tables
- Cognito User Pool
- Jenkins Server
- AWS CLI configured

---

# Example Application Flow

```text
User Login
   ↓
Cognito JWT Token
   ↓
Add Product To Cart
   ↓
Store Cart In DynamoDB
   ↓
Checkout Cart
   ↓
Create Order + OrderItems
   ↓
Fetch Orders History
```

---

# Planned Improvements

- Terraform Infrastructure as Code
- IAM least privilege policies
- AWS WAF integration
- Distributed tracing
- Dead Letter Queues (DLQ)
- SQS-based asynchronous checkout
- SNS notifications
- ECS/Fargate migration
- Kubernetes deployment
- Observability dashboards

---

# Future Enhancements

- Payment integration
- Inventory management
- Admin dashboard
- Email notifications
- Redis caching
- AI-based recommendations

---

# Author

## Sriram Chandra

AWS | DevOps | Cloud Engineering | Serverless Architecture | CI/CD Automation
