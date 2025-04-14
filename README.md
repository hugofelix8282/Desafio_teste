# Desafio Teste Prático 
## instruções do projeto 

### Realizar os testes
Instruçõees para realizar os testes através do bibioteca python-pytest. 
> a biblioteca testcontainers-python foi atribuída  para subir um banco de dados PostgreSQL isolado para os testes. logo, temos uma separação do  container postgres de desenvolvimento, do container testes. 

* No terminal raiz do seu projeto (conftest.py), rode:
```
pytest
```

* Obter  detalhes dos testes:
```
pytest -v
```
ver detalhes com print() incluído:
```
pytest -s
```  

### Docker 
Instruções para subir a aplicação via docker compose (ambiente de desenvolvimento). 
> observe que Para usar o Docker Compose, você precisa tê-lo instalado em seu sistema. Ele não está incluído na instalação padrão do Docker, então lembre-se de instalá-lo separadamente!

* No terminal, na raiz do projeto, execute:
```
docker-compose up --build  
```
* Para rodar em background:
```
docker-compose up -d --build
```
* Acesse sua aplicação no navegador:
```
http://localhost:8000/docs

```

###  Deploy da Aplicação na AWS com Docker e Terraform

Este projeto realiza o deploy de uma aplicação em **ambiente de produção** utilizando os seguintes serviços da **AWS**:

- EC2 (servidor de aplicação)
- RDS PostgreSQL (banco de dados gerenciado)
- VPC (rede isolada)
- S3 (armazenamento de arquivos, como logs, mídia ou backups)
- Docker + Docker Compose
- Terraform (provisionamento de infraestrutura)
- Variáveis de ambiente (.env)

---

#### 📦 Requisitos

- Conta na [AWS](https://aws.amazon.com/)
- `AWS CLI` configurado (`aws configure`)
- `Docker` e `Docker Compose` instalados
- `Terraform` instalado
- Chave SSH gerada e registrada na AWS EC2
- VPC padrão (ou personalizada via Terraform)

---

####  Arquitetura


---

####  Estrutura do Projeto 

```bash
.
├── Challenge_ProPig/
│   ├── main.py
│   └──  outros...
├── Dockerfile  
├── docker-compose.prod.yml  # (No seu docker-compose.prod, somente os serviços da aplicação deve estar presente.)
├── .env  # (Nunca habilitar no GitHub)
terraform/   
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── ec2/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── rds/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── s3/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│
├── env/
│   └── prod/
│       ├── main.tf
│       ├── variables.tf
│       ├── terraform.tfvars
│       ├── outputs.tf
│       ├── backend.tf
│       └── provider.tf
├── README.md

```

#### Provisionamento AWS com Terraform 

> Usar o Terraform para o provisionamento de infraestrutura na AWS (ou em qualquer nuvem) oferece vários benefícios práticos e estratégicos. Como descreve sua infraestrutura (instâncias EC2, RDS, VPCs, S3 etc.) em arquivos de configuração versionáveis, como código-fonte, Facilita automação, Permite versionamento com Git, Evita configuração manual no console da AWS (Não aconselhado). Então, vamos aos detalhes de cada arquivo.

##### terraform/main.tf

> Função: Define os recursos da infraestrutura que serão criados. É aqui que você declara:
* Instâncias EC2
* RDS (PostgreSQL)
* VPC
* S3
* Grupos de segurança (Security Groups)
* Endereços IP elásticos (EIP)
* Regras de firewall
* Provisões remotas (scripts que serão executados na EC2)

```
provider "aws" {
  region = var.region
}

# ----------------------------
# VPC, Subnet, e Internet Gateway
# ----------------------------

resource "aws_vpc" "main_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "MainVPC"
  }
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main_vpc.id

  tags = {
    Name = "MainInternetGateway"
  }
}

resource "aws_subnet" "public_subnet" {
  vpc_id                  = aws_vpc.main_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "PublicSubnet"
  }
}

resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "PublicRouteTable"
  }
}

resource "aws_route_table_association" "public_rt_assoc" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_rt.id
}

# ----------------------------
# S3 Bucket para armazenar arquivos/backups
# ----------------------------

resource "aws_s3_bucket" "app_bucket" {
  bucket = "app-prod-bucket-${random_id.suffix.hex}"

  versioning {
    enabled = true
  }

  tags = {
    Name = "AppBucket"
    Environment = "prod"
  }
}

resource "random_id" "suffix" {
  byte_length = 4
}

# ----------------------------
# Security Group para EC2 e RDS
# ----------------------------

resource "aws_security_group" "app_sg" {
  name   = "app_sg"
  vpc_id = aws_vpc.main_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "AppSG"
  }
}

# ----------------------------
# RDS PostgreSQL
# ----------------------------

resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "app-rds-subnet-group"
  subnet_ids = [aws_subnet.public_subnet.id]

  tags = {
    Name = "AppRDSSubnetGroup"
  }
}

resource "aws_db_instance" "app_db" {
  allocated_storage    = 20
  engine               = "postgres"
  engine_version       = "15"
  instance_class       = "db.t3.micro"
  name                 = "appdb"
  username             = var.db_username
  password             = var.db_password
  skip_final_snapshot  = true
  publicly_accessible  = true
  db_subnet_group_name = aws_db_subnet_group.rds_subnet_group.name
  vpc_security_group_ids = [aws_security_group.app_sg.id]

  tags = {
    Name = "AppRDS"
  }
}

# ----------------------------
# EC2 Instância
# ----------------------------

resource "aws_instance" "app_server" {
  ami                         = "ami-0fc5d935ebf8bc3bc"
  instance_type               = "t3.micro"
  key_name                    = var.key_name
  subnet_id                   = aws_subnet.public_subnet.id
  vpc_security_group_ids      = [aws_security_group.app_sg.id]
  associate_public_ip_address = true

  provisioner "remote-exec" {
    inline = [
      "sudo yum update -y",
      "sudo yum install docker git -y",
      "sudo service docker start",
      "sudo usermod -a -G docker ec2-user",
      "git clone https://github.com/seuusuario/seurepo.git app",
      "cd app && echo DATABASE_URL=postgresql://${var.db_username}:${var.db_password}@${aws_db_instance.app_db.address}:5432/appdb > .env",
      "cd app && docker-compose -f docker-compose.prod.yml up -d --build"
    ]

    connection {
      type        = "ssh"
      user        = "ec2-user"
      private_key = file("~/.ssh/id_rsa")
      host        = self.public_ip
    }
  }

  tags = {
    Name = "AppServer"
  }
}

# ----------------------------
# Outputs
# ----------------------------

output "ec2_public_ip" {
  value = aws_instance.app_server.public_ip
}

output "rds_endpoint" {
  value = aws_db_instance.app_db.address
}

output "s3_bucket_name" {
  value = aws_s3_bucket.app_bucket.bucket
}


```


##### terraform/variables.tf 

> Função: Define as variáveis reutilizáveis no projeto (e seus tipos). Ajuda a tornar o projeto flexível e fácil de configurar para diferentes ambientes.

```
variable "region" {
  default = "us-east-1"
}

variable "key_name" {
  description = "Nome da chave SSH"
}

variable "db_username" {
  default = "admin"
}

variable "db_password" {
  description = "Senha do banco de dados"
  sensitive   = true
}
```

##### terraform/outputs.tf

> Função: Exibe informações úteis após o deploy. Essas saídas ajudam a copiar facilmente o IP da EC2, o endpoint do RDS etc.

```
voutput "ec2_ip" {
  value = aws_instance.app.public_ip
}

output "rds_endpoint" {
  value = aws_db_instance.db.endpoint
}

```

##### terraform/provider.tf (opcional, mas recomendado)

> unção: Define o provedor de nuvem que será usado (ex: AWS, Azure, GCP).

```
provider "aws" {
  region = var.region
  profile = "default"  # se você usa perfis no AWS CLI
}

```

##### Boas Práticas Adicionais

* backend.tf	(Define o armazenamento do estado remoto (S3 + DynamoDB))
* versions.tf	(Restringe as versões do Terraform e providers)
* modules/	(Separar blocos reutilizáveis como vpc, ec2, rds)
* env/dev/ ( env/prod/	Permite ambientes isolados e organizados)

#####   Executar o Terraform

> Seguindo a cultura Devops é aconselhado nunca executar o terraform localmente em produção. Utilizar  uma pipeline CI/CD (como GitHub Actions, GitLab CI, Jenkins). Normalmente aplico a execução do terraform via Jenkins. Tal definição deixarei para os próximos desafioes.

 












