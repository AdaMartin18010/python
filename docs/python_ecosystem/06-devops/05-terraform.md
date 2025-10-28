# Terraform 基础设施即代码

**Python应用基础设施自动化管理**

---

## 📋 概述

Terraform是HashiCorp开发的IaC（Infrastructure as Code）工具，用于安全高效地构建、更改和版本化基础设施。

### 核心特性

- 📝 **声明式** - HCL配置语言
- 🌐 **多云支持** - AWS、Azure、GCP等
- 📊 **状态管理** - 跟踪资源状态
- 🔄 **变更计划** - 预览变更
- 🔧 **模块化** - 可重用配置

---

## 🚀 快速开始

### 安装

```bash
# macOS
brew install terraform

# Linux
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/
```

### 基础配置

```hcl
# main.tf
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "python-app/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}
```

---

## 🏗️ 部署Python应用

### EC2实例

```hcl
# ec2.tf
resource "aws_instance" "app_server" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.instance_type
  key_name      = aws_key_pair.deployer.key_name
  
  vpc_security_group_ids = [aws_security_group.app_sg.id]
  subnet_id              = aws_subnet.public.id
  
  user_data = templatefile("${path.module}/user_data.sh", {
    app_version = var.app_version
  })
  
  tags = {
    Name        = "python-app-${var.environment}"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# 安全组
resource "aws_security_group" "app_sg" {
  name        = "python-app-sg"
  description = "Security group for Python app"
  vpc_id      = aws_vpc.main.id
  
  # HTTP
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # HTTPS
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  # SSH
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.admin_cidr]
  }
  
  # Outbound
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# User data脚本
# user_data.sh
#!/bin/bash
set -e

# 更新系统
apt-get update
apt-get install -y python3 python3-pip python3-venv nginx

# 创建应用目录
mkdir -p /opt/app
cd /opt/app

# 下载应用
aws s3 cp s3://my-app-bucket/app-${app_version}.tar.gz .
tar -xzf app-${app_version}.tar.gz

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 配置systemd
cat > /etc/systemd/system/app.service <<EOF
[Unit]
Description=Python App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/app
Environment="PATH=/opt/app/venv/bin"
ExecStart=/opt/app/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 启动服务
systemctl daemon-reload
systemctl enable app
systemctl start app

# 配置nginx
cat > /etc/nginx/sites-available/app <<EOF
server {
    listen 80;
    server_name _;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

ln -sf /etc/nginx/sites-available/app /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
systemctl reload nginx
```

---

## 🗄️ RDS数据库

```hcl
# rds.tf
resource "aws_db_instance" "app_db" {
  identifier        = "python-app-db"
  engine            = "postgres"
  engine_version    = "15.3"
  instance_class    = var.db_instance_class
  allocated_storage = 20
  
  db_name  = "appdb"
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.db_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = var.environment != "production"
  
  tags = {
    Name        = "python-app-db-${var.environment}"
    Environment = var.environment
  }
}

resource "aws_security_group" "db_sg" {
  name        = "python-app-db-sg"
  description = "Security group for database"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app_sg.id]
  }
}
```

---

## ⚖️ 负载均衡器

```hcl
# alb.tf
resource "aws_lb" "app" {
  name               = "python-app-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = aws_subnet.public[*].id
  
  tags = {
    Name        = "python-app-alb"
    Environment = var.environment
  }
}

resource "aws_lb_target_group" "app" {
  name     = "python-app-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
  
  health_check {
    enabled             = true
    path                = "/health"
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 5
    interval            = 30
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.app.arn
  port              = 80
  protocol          = "HTTP"
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app.arn
  }
}

# Auto Scaling Group
resource "aws_autoscaling_group" "app" {
  name                = "python-app-asg"
  vpc_zone_identifier = aws_subnet.private[*].id
  target_group_arns   = [aws_lb_target_group.app.arn]
  health_check_type   = "ELB"
  
  min_size         = var.min_instances
  max_size         = var.max_instances
  desired_capacity = var.desired_instances
  
  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }
  
  tag {
    key                 = "Name"
    value               = "python-app-instance"
    propagate_at_launch = true
  }
}
```

---

## 📊 变量和输出

### 变量定义

```hcl
# variables.tf
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "production"], var.environment)
    error_message = "Environment must be dev, staging, or production."
  }
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.medium"
}

variable "app_version" {
  description = "Application version to deploy"
  type        = string
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
```

### 变量文件

```hcl
# terraform.tfvars
aws_region     = "us-east-1"
environment    = "production"
instance_type  = "t3.large"
app_version    = "1.0.0"

# production.tfvars
min_instances     = 2
max_instances     = 10
desired_instances = 3
db_instance_class = "db.t3.large"
```

### 输出定义

```hcl
# outputs.tf
output "alb_dns_name" {
  description = "ALB DNS name"
  value       = aws_lb.app.dns_name
}

output "rds_endpoint" {
  description = "RDS endpoint"
  value       = aws_db_instance.app_db.endpoint
  sensitive   = true
}

output "instance_ids" {
  description = "EC2 instance IDs"
  value       = aws_instance.app_server[*].id
}
```

---

## 📦 模块化

### 创建模块

```
modules/
└── python-app/
    ├── main.tf
    ├── variables.tf
    ├── outputs.tf
    └── README.md
```

```hcl
# modules/python-app/main.tf
resource "aws_instance" "app" {
  count = var.instance_count
  
  ami           = var.ami_id
  instance_type = var.instance_type
  
  tags = merge(
    var.common_tags,
    {
      Name = "${var.app_name}-${count.index}"
    }
  )
}
```

### 使用模块

```hcl
# main.tf
module "python_app" {
  source = "./modules/python-app"
  
  app_name       = "myapp"
  instance_count = 3
  instance_type  = "t3.medium"
  ami_id         = data.aws_ami.ubuntu.id
  
  common_tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
```

---

## 🔄 工作流程

### 基础命令

```bash
# 初始化
terraform init

# 验证配置
terraform validate

# 格式化代码
terraform fmt -recursive

# 规划变更
terraform plan -out=tfplan

# 应用变更
terraform apply tfplan

# 查看状态
terraform show

# 销毁资源
terraform destroy
```

### Workspace管理

```bash
# 创建workspace
terraform workspace new staging
terraform workspace new production

# 切换workspace
terraform workspace select production

# 列出workspace
terraform workspace list

# 当前workspace
terraform workspace show
```

---

## 🐍 Python集成

### 使用python-terraform

```bash
pip install python-terraform
```

```python
from python_terraform import Terraform, IsFlagged

# 初始化
tf = Terraform(working_dir='./terraform')
tf.init()

# 规划
return_code, stdout, stderr = tf.plan(
    var={'environment': 'production', 'app_version': '1.0.0'}
)

# 应用
return_code, stdout, stderr = tf.apply(
    skip_plan=True,
    var={'environment': 'production', 'app_version': '1.0.0'}
)

# 获取输出
alb_dns = tf.output('alb_dns_name')
print(f"ALB DNS: {alb_dns}")

# 销毁
tf.destroy(auto_approve=IsFlagged)
```

---

## 📚 最佳实践

### 1. 状态管理

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "env/${var.environment}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-lock"
  }
}
```

### 2. 敏感数据

```hcl
# 使用环境变量
export TF_VAR_db_password="SuperSecret123"

# 或AWS Secrets Manager
data "aws_secretsmanager_secret_version" "db_password" {
  secret_id = "prod/db/password"
}

resource "aws_db_instance" "app_db" {
  password = data.aws_secretsmanager_secret_version.db_password.secret_string
}
```

### 3. 目录结构

```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   │   ├── main.tf
│   │   └── terraform.tfvars
│   └── production/
│       ├── main.tf
│       └── terraform.tfvars
├── modules/
│   ├── networking/
│   ├── compute/
│   └── database/
└── global/
    ├── iam/
    └── s3/
```

---

## 🔗 相关资源

- [Terraform文档](https://www.terraform.io/docs)
- [Terraform Registry](https://registry.terraform.io/)

---

**最后更新**: 2025年10月28日

