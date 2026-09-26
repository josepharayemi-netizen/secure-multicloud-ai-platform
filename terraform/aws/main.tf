locals {
  name = "secure-ai-${var.environment}"
  tags = {Project = "secure-multicloud-ai-platform", Environment = var.environment, ManagedBy = "Terraform"}
}
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"
  name = local.name
  cidr = "10.40.0.0/16"
  azs = ["${var.region}a", "${var.region}b"]
  private_subnets = ["10.40.1.0/24", "10.40.2.0/24"]
  public_subnets = ["10.40.101.0/24", "10.40.102.0/24"]
  enable_nat_gateway = true
  single_nat_gateway = true
}
module "eks" {
  source = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"
  cluster_name = local.name
  cluster_version = var.cluster_version
  cluster_endpoint_public_access = false
  cluster_endpoint_private_access = true
  enable_irsa = true
  vpc_id = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  eks_managed_node_groups = {
    platform = {
      instance_types = ["t3.large"]
      min_size = 2
      max_size = 5
      desired_size = 2
    }
  }
}
resource "aws_kms_key" "platform" {
  description = "Secure AI platform artifact encryption"
  enable_key_rotation = true
}
resource "aws_s3_bucket" "artifacts" {bucket_prefix = "${local.name}-artifacts-"}
resource "aws_s3_bucket_public_access_block" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}
resource "aws_s3_bucket_server_side_encryption_configuration" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.platform.arn
      sse_algorithm = "aws:kms"
    }
  }
}
resource "aws_ecr_repository" "api" {
  name = local.name
  image_tag_mutability = "IMMUTABLE"
  image_scanning_configuration {scan_on_push = true}
  encryption_configuration {encryption_type = "KMS"; kms_key = aws_kms_key.platform.arn}
}
