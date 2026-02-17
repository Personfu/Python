# RDS, ECS, and ALB Infrastructure
# CIS 410 — Cloud & DevOps | Preston Furulie

# --- RDS MySQL Instance ---

resource "aws_db_subnet_group" "db" {
  name       = "guitar-shop-db-subnet"
  subnet_ids = [aws_subnet.private_a.id, aws_subnet.private_b.id]

  tags = { Name = "guitar-shop-db-subnet-group" }
}

resource "aws_security_group" "db" {
  name        = "db-sg"
  description = "Allow MySQL from app layer only"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 3306
    to_port         = 3306
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }
}

resource "aws_db_instance" "mysql" {
  identifier              = "guitar-shop-db"
  engine                  = "mysql"
  engine_version          = "8.0"
  instance_class          = "db.t3.medium"
  allocated_storage       = 50
  storage_encrypted       = true
  multi_az                = true
  db_name                 = "guitar_shop"
  username                = "admin"
  password                = var.db_password
  db_subnet_group_name    = aws_db_subnet_group.db.name
  vpc_security_group_ids  = [aws_security_group.db.id]
  backup_retention_period = 30
  skip_final_snapshot     = false

  tags = { Name = "guitar-shop-rds" }
}

# --- ECS Cluster & Service ---

resource "aws_ecs_cluster" "main" {
  name = "guitar-shop-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_security_group" "app" {
  name        = "app-sg"
  description = "Allow traffic from ALB only"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port       = 3000
    to_port         = 3000
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ecs_task_definition" "api" {
  family                   = "guitar-shop-api"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.ecs_execution.arn

  container_definitions = jsonencode([{
    name      = "api"
    image     = "guitar-shop-api:latest"
    essential = true
    portMappings = [{
      containerPort = 3000
      protocol      = "tcp"
    }]
    environment = [
      { name = "DB_HOST", value = aws_db_instance.mysql.address },
      { name = "DB_NAME", value = "guitar_shop" },
      { name = "NODE_ENV", value = "production" }
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/guitar-shop-api"
        "awslogs-region"        = "us-west-2"
        "awslogs-stream-prefix" = "ecs"
      }
    }
  }])
}

resource "aws_ecs_service" "api" {
  name            = "guitar-shop-api"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = [aws_subnet.private_a.id, aws_subnet.private_b.id]
    security_groups = [aws_security_group.app.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "api"
    container_port   = 3000
  }
}

# --- Application Load Balancer ---

resource "aws_security_group" "alb" {
  name        = "alb-sg"
  description = "Allow HTTP/HTTPS from internet"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_lb" "main" {
  name               = "guitar-shop-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = [aws_subnet.public_a.id, aws_subnet.public_b.id]
}

resource "aws_lb_target_group" "api" {
  name        = "guitar-shop-api-tg"
  port        = 3000
  protocol    = "HTTP"
  vpc_id      = aws_vpc.main.id
  target_type = "ip"

  health_check {
    path                = "/api/health"
    healthy_threshold   = 2
    unhealthy_threshold = 3
    interval            = 30
  }
}

resource "aws_lb_listener" "https" {
  load_balancer_arn = aws_lb.main.arn
  port              = 443
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-TLS13-1-2-2021-06"
  certificate_arn   = var.ssl_certificate_arn

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.api.arn
  }
}

# --- Variables ---

variable "db_password" {
  type      = string
  sensitive = true
}

variable "ssl_certificate_arn" {
  type = string
}
