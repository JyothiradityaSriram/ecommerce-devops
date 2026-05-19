resource "aws_ecs_cluster" "cluster" {
  name = "cart-cluster"
}

resource "aws_ecs_task_definition" "task" {
  family                   = "cart-task"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "512"

  task_role_arn      = aws_iam_role.ecs_task_role.arn
  execution_role_arn = aws_iam_role.ecs_execution_role.arn

  container_definitions = jsonencode([
    {
      name  = "cart"
      image = "542175649814.dkr.ecr.ap-south-1.amazonaws.com/cart-service:latest"

      portMappings = [{
        containerPort = 5000
      }]

      environment = [
        { name = "AWS_REGION", value = "ap-south-1" },
        { name = "CART_TABLE", value = "cart" },
        { name = "JWT_SECRET", value = "secret" },
        { name = "ENV", value = "prod" }
      ]
    }
  ])
}

resource "aws_security_group" "ecs_sg" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port       = 5000
    to_port         = 5000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb_sg.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ecs_service" "service" {
  name            = "cart-service"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.task.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = [
      aws_subnet.public_1.id,
      aws_subnet.public_2.id
    ]
    assign_public_ip = true
    security_groups  = [aws_security_group.ecs_sg.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.tg.arn
    container_name   = "cart"
    container_port   = 5000
  }
}
